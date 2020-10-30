import json
import time
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    try:
        
    
        client = boto3.resource('dynamodb')
        table = client.Table('WishmMiners')
        epochSub31days=int(time.time()) - (31*24*60*60*1000)
        response = table.query(
             # Users who were not active from the past 31 days

            IndexName = 'userStatus-lastSeenTime-index',
            KeyConditionExpression=Key('userStatus').eq(0) & Key('lastSeenTime').gt(epochSub31days),
        )
        
        items=response['Items']
        
        for item in items:
            
            # deleting the users
            resp=table.delete_item(
                Key={'userId':item['userId']}
            )
            
    except Exception as e:
        print(e)
            