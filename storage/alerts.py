import boto3
import logging
from typing import List
from botocore.exceptions import ClientError
from config.config import Config


class SentAlerts:
    def __init__(self):
        self.config: Config = Config()
        self.dynamodb = boto3.resource("dynamodb")
        self.alerts_table = self.dynamodb.Table("SentAlerts")
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def alert_already_sent(self, alert_id: str) -> bool:
        try:
            response = self.alerts_table.get_item(Key={"ID": alert_id})
            return "Item" in response
        except ClientError as e:
            self.logger.error(f"Error checking DynamoDB: {e}")
            raise

    def store_sent_alerts(self, alert_ids: List[str]) -> None:
        try:
            with self.alerts_table.batch_writer() as batch:
                for alert_id in alert_ids:
                    batch.put_item(Item={"ID": alert_id})
            self.logger.info(f"Stored alerts for IDs: {alert_ids}")
        except ClientError as e:
            self.logger.error(f"Error storing alerts in DynamoDB: {e}")
            raise
