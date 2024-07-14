import boto3
import logging
from botocore.exceptions import ClientError
from phonenumbers import is_valid_number, parse

dynamodb = boto3.resource('dynamodb')
subscribers_table = dynamodb.Table('Subscribers')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def add_subscriber(phone_number):
    if not is_valid_number(parse(phone_number, "US")):
        logger.info(f"Phone number {phone_number} is invalid.")
        return
    
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
