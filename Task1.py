import time
import json
import boto3
from boto3.dynamodb.conditions import Key
# from botocore.exceptions import ClientError
import botocore.exceptions
def lambda_handler(event, context):
    try:
        client = boto3.resource('dynamodb')
        table = client.Table('WishmMiners')
        epochSub7days = int(time.time()) - (7*24*60*60)
        
        response = table.query(
        
            IndexName = 'userStatus-lastSeenTime-index',
            # Users who were not active from the past 7 days
            KeyConditionExpression = Key('userStatus').eq(0) & Key('lastSeenTime').gt(epochSub7days),
        )
        
        # Sending emails to the users for reminder
        ses = boto3.client('ses')
        body = '''
            hello user, hope you are doing great
            
            thanks'''
            
        
        
        items=response['Items']
        for item in items:
            
            # Updating the userStatus 
            table.update_item(
                Key = {
                    
                    'userId': item['userId'],
                },
            UpdateExpression = "set userStatus = :g",
            ExpressionAttributeValues={
                    ':g': 2
                },
            )
            a=ses.send_email(
                Source='mayank.maheshwari625@gmail.com',
                Destination={
                        'ToAddresses':[
                             item['email'],
                         ]
                },
            
                
                Message={
                    'Subject':{
                        'Data':'SES Demo',
                        'Charset':'UTF-8'
                    },
                    'Body':{
                        'Text':{
                            'Data':body,
                            'Charset':'UTF-8'
                        }
                    }
                }
            )
            
        
    except Exception as e:
        print(e)