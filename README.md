<h1 align="center">
    CRUD Application Integrated with EC2, DynamoDB, and S3
</h1>

This is a project intergated with EC2, DynamoDB, and S3. We wanted to understand a few services offered by AWS and develop a good understanding of the security behind them.

## Technologies Used

- [Python](https://www.python.org/)
- [FlaskAPI](https://flask.palletsprojects.com/en/stable/)
- [EC2 Instance](https://aws.amazon.com/ec2/)
- [DynamoDB](https://aws.amazon.com/dynamodb/)
- [S3 Bucket](https://aws.amazon.com/s3/)

## Development

1. To get started, you must log into AWS and start a DynamoDB table.
2. Change lines 9 and 10 in app.py to the correct configurations of the table.
3. Start up a S3 bucket on AWS
4. Change lines 13 and 14 in app.py to the correct configurations of the bucket.

## Directions To Run The Application

To run the application:

1. You must log into AWS and spin up an EC2 instance.
2. SSH into that instance and transfer this folder over.
3. Run the Flask API by running

```
python3 app.py
```

in the same directory as app.py

4. Then go to the public IP address with port 5000.

You now should be able to perform all operations in the web application.
