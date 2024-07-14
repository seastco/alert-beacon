import logging
from src.usgs_api import get_recent_earthquakes
from src.dynamodb import get_subscribers, alert_already_sent, store_sent_alert
from src.alert import send_alert

def lambda_handler(event, context):
    earthquakes = get_recent_earthquakes()
    
    if not earthquakes:
        return
    
    subscribers = get_subscribers()
    
    for earthquake in earthquakes:
        if not alert_already_sent(earthquake['id']):
            send_alert(earthquake, subscribers)
            store_sent_alert(earthquake['id'])
