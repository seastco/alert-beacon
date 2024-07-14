import logging
from src.usgs_api import get_recent_earthquakes
from src.dynamodb import get_subscribers, alert_already_sent, store_sent_alert
from src.alert import send_alert

logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    try:
        earthquakes = get_recent_earthquakes()
        if not earthquakes:
            return
        
        subscribers = get_subscribers()
        
        for earthquake in earthquakes:
            if not alert_already_sent(earthquake['id']):
                send_alert(earthquake, subscribers)
                logger.info(f'Alert for earthquake {earthquake["id"]} sent successfully')
                store_sent_alert(earthquake['id'])
        
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return {'statusCode': 500, 'body': f'Internal server error: {str(e)}'}
