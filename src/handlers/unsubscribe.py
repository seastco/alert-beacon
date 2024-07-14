from src.dynamodb import remove_subscriber
import logging

logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    phone_number = event.get('phone_number')
    if not phone_number:
        return {
            'statusCode': 400,
            'body': 'Phone number is required'
        }

    try:
        remove_subscriber(phone_number)
        return {
            'statusCode': 200,
            'body': f'Successfully unsubscribed {phone_number}'
        }
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return {
            'statusCode': 500,
            'body': f'Internal server error: {str(e)}'
        }
