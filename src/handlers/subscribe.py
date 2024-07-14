import logging
from validate import validate_request, ValidationError
from src.dynamodb import add_subscriber

logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    try:
        phone_number = validate_request(event)
        add_subscriber(phone_number)
        return {'statusCode': 200, 'body': f'Successfully subscribed {phone_number}'}
    except ValidationError as e:
        return {'statusCode': e.status_code, 'body': e.message}
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return {'statusCode': 500, 'body': f'Internal server error: {str(e)}'}