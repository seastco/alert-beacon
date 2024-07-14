import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# DynamoDB configuration
dynamodb = boto3.resource('dynamodb')
subscribers_table = dynamodb.Table('Subscribers')
alerts_table = dynamodb.Table('SentAlerts')

def get_subscribers():
    try:
        response = subscribers_table.scan()
        return [item['PhoneNumber'] for item in response['Items']]
    except ClientError as e:
        logger.error(f"Error fetching subscribers: {e}")
        return []

def store_sent_alert(earthquake_id):
    try:
        alerts_table.put_item(Item={'EarthquakeID': earthquake_id})
        logger.info(f"Stored alert for earthquake ID: {earthquake_id}")
    except ClientError as e:
        logger.error(f"Error storing alert in DynamoDB: {e}")

def alert_already_sent(earthquake_id):
    try:
        response = alerts_table.get_item(Key={'EarthquakeID': earthquake_id})
        return 'Item' in response
    except ClientError as e:
        logger.error(f"Error checking DynamoDB: {e}")
        return False
