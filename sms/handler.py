import json
from twilio.twiml.messaging_response import MessagingResponse
from storage.subscribers import Subscribers
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        request = event.get("request")
        message = request["body"]
        message = message.strip().upper()
        from_number = request["from"]
        subscribers = Subscribers()
        resp = MessagingResponse()

        if message == "SHEEBA":
            subscribers.add_subscriber(from_number)
            resp.message("You have successfully subscribed to Tectonic Alert!")
        elif message == "UNSHEEBA":
            subscribers.remove_subscriber(from_number)
            resp.message("You have unsubscribed from Tectonic Alert.")
        else:
            # No-op
            return {"statusCode": 200}
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/xml"},
            "body": str(resp),
        }
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
