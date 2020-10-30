import json
import time
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('WishmMiners')
    epochSub1hr = int(time.time()) - (60*60*1000)
    try:
        
    
        response = table.query(
            # Users who didn't the pay within 1 hour

            IndexName = 'userStatus-lpu-index',
            KeyConditionExpression = Key('userStatus').eq(0) & Key('lpu').gt(epochSub1hr),
        )
        items=response['Items']
        for item in items:
            
            # deleting the users

            resp=table.delete_item(
                Key={'userId':item['userId']}
            )
            
    except Exception as e:
        print(e)       
                