from src.dynamodb import add_subscriber
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    phone_number = event.get('phone_number')
    if not phone_number:
        return {
            'statusCode': 400,
            'body': 'Phone number is required'
        }

    try:
        add_subscriber(phone_number)
        return {
            'statusCode': 200,
            'body': f'Successfully subscribed {phone_number}'
        }
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return {
            'statusCode': 500,
            'body': f'Internal server error: {str(e)}'
        }
