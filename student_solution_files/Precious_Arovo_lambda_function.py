"""
Precious-Arovo-Cloud-Computing-Predict-Lambda-Function
"""

import boto3    # Python AWS SDK
import json     # Used for handling API-based data.
import base64   # Needed to decode the incoming POST data
import random   # Needed to create a random value
from botocore.exceptions import ClientError # Catch errors on client side

def lambda_handler(event, context):
    
    # Perform JSON data decoding 
    body_enc = event['body']
    dec_dict = json.loads(base64.b64decode(body_enc))
    #dec_dict = event
    
    
    # --- Write to dynamodb ---
    
    # Instantiating a random value from 1 to 1,000,000,000.
    rid = random.randint(1, 1000000000) 
    # -----------------------------
    
    # ** Instantiating the DynamoDB service with the help of the boto3 library **

    dynamodb = dynamodb.resource('dynamodb')
    # -----------------------------
    
    # Instantiating the Dynamodb Table already created in step 4.
    table = dynamodb.Table('Precious-Arovo-Portfolio-Data')
    

    # ** Writing the responses to the table using the put_item method. **
    # incoming data is sent to the matching column in your DynamoDB table
    db_response = table.put_item(Item={'ResponsesID': rid,
                        'Name': dec_dict['name'],
                        'Email': dec_dict['email'],
                        'Cell': dec_dict['phone'],
                        'Message': dec_dict['message']
    })
    # -----------------------------


    # Sample text that you would like to email to your recipient address from your sender address.
    email_text = 'Insert your sample email here'

    # ** SES Functionality **

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = 'arovoprecious@gmail.com'
    # -----------------------------

    # Replace recipient@example.com with a "To" address.
    RECIPIENT = 'arovoprecious@gmail.com' 
    # -----------------------------


    # The unmodified subject line for the email.
    SUBJECT = f"Data Science Portfolio Project Website - Hello {dec_dict['name']}"
    # -------------------------------

    # The email body for recipients with non-HTML email clients
    BODY_TEXT = (email_text)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES service resource
    client = boto3.client('ses')

    # Try to send the email.
    try:
        #Provide the contents of the email.
        ses_response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                    # 'edsa.predicts@explore-ai.net', # <--- Uncomment this line once you have successfully tested your predict end-to-end
                ],
            },
            Message={
                'Body': {

                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )

    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(ses_response['MessageId'])



    # ** Create a response object to inform the website that the workflow executed successfully. **
    lambda_response = {
        'statusCode': 200,
        'body': json.dumps({
        'Name': dec_dict['name'],
        'Email': dec_dict['email'],
        'Cell': dec_dict['phone'], 
        'Message': dec_dict['message'],
        'DB_response': db_response
        })
    }
    
    return lambda_response