import boto3
import logging
import os
from botocore.exceptions import ClientError

class StorageService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.subscribers_table = self.dynamodb.Table('Subscribers')
        self.alerts_table = self.dynamodb.Table('SentAlerts')
        self.environment = os.getenv('ENVIRONMENT', 'prod')
        self.test_subscribers = os.getenv('TEST_SUBSCRIBERS', '').split(',')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def get_subscribers(self):
        if self.environment != 'prod':
            return self.test_subscribers

        try:
            response = self.subscribers_table.scan()
            return [item['PhoneNumber'] for item in response['Items']]
        except ClientError as e:
            self.logger.error(f"Error fetching subscribers: {e}")
            raise

    def alert_already_sent(self, alert_id):
        try:
            response = self.alerts_table.get_item(Key={'ID': alert_id})
            return 'Item' in response
        except ClientError as e:
            self.logger.error("Error checking DynamoDB: {e}")
            raise

    def store_sent_alert(self, alert_id):
        try:
            self.alerts_table.put_item(Item={'ID': alert_id})
            self.logger.info(f"Stored alert for ID: {alert_id}")
        except ClientError as e:
            self.logger.error(f"Error storing alert in DynamoDB: {e}")
            raise
