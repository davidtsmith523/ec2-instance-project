from flask import Flask, render_template, request, redirect, url_for
import boto3

app = Flask(__name__)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('TestTable')

# Home page (Read operation)
@app.route('/')
def index():
    response = table.scan()
    items = response['Items']
    return render_template('index.html', items=items)

# Create operation
@app.route('/create', methods=['POST'])
def create_item():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        
        # Insert item into DynamoDB
        table.put_item(
            Item={
                'id': id,
                'name': name,
                'email': email
            }
        )
        return redirect(url_for('index'))

# Update operation
@app.route('/update/<string:id>', methods=['GET', 'POST'])
def update_item(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Update item in DynamoDB
        table.update_item(
            Key={'id': id},
            UpdateExpression="SET #n = :name, email = :email",
            ExpressionAttributeNames={
                '#n': 'name'
            },
            ExpressionAttributeValues={
                ':name': name,
                ':email': email
            }
        )
        return redirect(url_for('index'))
    
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
