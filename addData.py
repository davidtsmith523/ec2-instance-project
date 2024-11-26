import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table('TestTable')

def add_item(item_data):
    response = table.put_item(Item=item_data)
    return response

# Example usage
if __name__ == "__main__":
    item = {
        'id': '123',
        'name': 'John Doe',
        'email': 'johndoe@example.com'
    }
    print(add_item(item))
