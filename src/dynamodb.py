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

def add_subscriber(phone_number):
    try:
        subscribers_table.put_item(
            Item={'PhoneNumber': phone_number},
            ConditionExpression='attribute_not_exists(PhoneNumber)'
        )
        logger.info(f"Added subscriber: {phone_number}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            logger.info(f"Subscriber {phone_number} already exists.")
        else:
            logger.error(f"Error adding subscriber: {e}")
            raise

def remove_subscriber(phone_number):
    try:
        subscribers_table.delete_item(Key={'PhoneNumber': phone_number})
        logger.info(f"Removed subscriber: {phone_number}")
    except ClientError as e:
        logger.error(f"Error removing subscriber: {e}")
        raise

def alert_already_sent(earthquake_id):
    try:
        response = alerts_table.get_item(Key={'EarthquakeID': earthquake_id})
        return 'Item' in response
    except ClientError as e:
        logger.error(f"Error checking DynamoDB: {e}")
        return False

def store_sent_alert(earthquake_id):
    try:
        alerts_table.put_item(Item={'EarthquakeID': earthquake_id})
        logger.info(f"Stored alert for earthquake ID: {earthquake_id}")
    except ClientError as e:
        logger.error(f"Error storing alert in DynamoDB: {e}")
