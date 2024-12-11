from flask import Flask, render_template, request, redirect, url_for
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('TestTable')

# Initialize S3 client
s3 = boto3.client('s3', region_name='us-east-1')
BUCKET_NAME = 'my-s3-test-bucket-test-123'

# Home page (Read operation)
@app.route('/')
def index():
    response = table.scan()
    items = response['Items']
    return render_template('index.html', items=items)

# Create operation
@app.route('/create', methods=['POST'])
def create_item():
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    file = request.files['image']  # Image file from the form

    if file:
        # Secure the filename and upload to S3
        filename = secure_filename(file.filename)
        s3.upload_fileobj(file, BUCKET_NAME, filename)
        image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
    else:
        image_url = None

    # Insert item into DynamoDB
    table.put_item(
        Item={
            'id': id,
            'name': name,
            'email': email,
            'image_url': image_url  # Save image URL in DynamoDB
        }
    )
    return redirect(url_for('index'))

# Update operation
@app.route('/update/<string:id>', methods=['GET', 'POST'])
def update_item(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        file = request.files['image']  # Optional new image file from the form

        if file:
            # Secure the filename and upload to S3
            filename = secure_filename(file.filename)
            s3.upload_fileobj(file, BUCKET_NAME, filename)
            image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
        else:
            image_url = request.form['current_image_url']  # Keep the existing image URL

        # Update item in DynamoDB
        table.update_item(
            Key={'id': id},
            UpdateExpression="SET #n = :name, email = :email, image_url = :image_url",
            ExpressionAttributeNames={
                '#n': 'name'
            },
            ExpressionAttributeValues={
                ':name': name,
                ':email': email,
                ':image_url': image_url
            }
        )
        return redirect(url_for('index'))

    # Fetch item for pre-filling the update form
    response = table.get_item(Key={'id': id})
    item = response.get('Item')
    return render_template('update_item.html', item=item)

# Delete operation
@app.route('/delete/<string:id>', methods=['GET'])
def delete_item(id):
    table.delete_item(Key={'id': id})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
