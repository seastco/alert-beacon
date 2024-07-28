import logging
from alerts.handler import lambda_handler as alerts_handler
from sms.handler import lambda_handler as sms_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(f"Received event: {event}")

    try:
        handler_type = event.get("handler")

        if not handler_type:
            logger.error("No handler type specified.")
            return {"statusCode": 400, "body": "No handler type specified"}
        if handler_type == "alerts":
            return alerts_handler(event, context)
        elif handler_type == "sms":
            return sms_handler(event, context)
        else:
            logger.error("Invalid handler type specified.")
            return {"statusCode": 400, "body": "Invalid handler type specified"}

    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        return {"statusCode": 500, "body": f"Internal server error: {str(e)}"}
