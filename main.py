import logging
from services.alert_manager import AlertManager

logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    try:
        alert_manager = AlertManager()
        alert_types = ["earthquake"]
        alert_manager.process_alerts(alert_types)
        return {"statusCode": 200}
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return {"statusCode": 500, "body": f"Internal server error: {str(e)}"}


if __name__ == "__main__":
    lambda_handler(None, None)
