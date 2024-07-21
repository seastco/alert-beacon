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
            self.logger.error(f"Error checking DynamoDB: {e}")
            raise

    def store_sent_alerts(self, alert_ids):
        try:
            with self.alerts_table.batch_writer() as batch:
                for alert_id in alert_ids:
                    batch.put_item(Item={'ID': alert_id})
            self.logger.info(f"Stored alerts for IDs: {alert_ids}")
        except ClientError as e:
            self.logger.error(f"Error storing alerts in DynamoDB: {e}")
            raise
