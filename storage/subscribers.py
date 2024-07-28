import boto3
import logging
from typing import List
from botocore.exceptions import ClientError
from config.config import Config
from phonenumbers import is_valid_number, parse


class Subscribers:
    def __init__(self):
        self.config: Config = Config()
        self.dynamodb = boto3.resource("dynamodb")
        self.subscribers_table = self.dynamodb.Table("Subscribers")
        self.environment: str = self.config.get("ENVIRONMENT")
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def add_subscriber(self, phone_number):
        if not is_valid_number(parse(phone_number, "US")):
            self.logger.info(f"Phone number {phone_number} is invalid.")
            return

        try:
            self.subscribers_table.put_item(
                Item={"PhoneNumber": phone_number},
                ConditionExpression="attribute_not_exists(PhoneNumber)",
            )
            self.logger.info(f"Added subscriber: {phone_number}")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                self.logger.info(f"Subscriber {phone_number} already exists.")
            else:
                self.logger.error(f"Error adding subscriber: {e}")
                raise

    def remove_subscriber(self, phone_number):
        try:
            self.subscribers_table.delete_item(Key={"PhoneNumber": phone_number})
            self.logger.info(f"Removed subscriber: {phone_number}")
        except ClientError as e:
            self.logger.error(f"Error removing subscriber: {e}")
            raise

    def get_subscribers(self) -> List[str]:
        if self.environment != "prod":
            return self.test_subscribers
        try:
            response = self.subscribers_table.scan()
            return [item["PhoneNumber"] for item in response["Items"]]
        except ClientError as e:
            self.logger.error(f"Error fetching subscribers: {e}")
            raise
