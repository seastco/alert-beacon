import os
import logging
import pytz
from datetime import datetime
from twilio.rest import Client

logger = logging.getLogger(__name__)

# Twilio configuration
TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE = os.environ["TWILIO_PHONE"]

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_alert(earthquake, subscribers):
    formatted_time = _get_formatted_time(earthquake['properties']['time'])
    message = f"ALERT! {earthquake['properties']['mag']} magnitude earthquake detected {earthquake['properties']['place']} at {formatted_time}"
    
    for phone in subscribers:
        if not send_sms(phone, message):
            logger.error(f"Failed to send alert to {phone}.")
            return False
    
    return True

def send_sms(phone, message):
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=phone
        )
        logger.info(f"Sent alert to phone {phone}: {message}")
        return True
    except Exception as e:
        logger.error(f"Error sending alert to phone {phone}: {e}")
        return False
    
def _get_formatted_time(timestamp):
    utc_time = datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc)
    pacific_time = utc_time.astimezone(pytz.timezone('US/Pacific'))
    return pacific_time.strftime("%I:%M %p %Z")
