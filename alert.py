import os
import requests
import time
import logging
import pytz
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Twilio configuration
TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
RECIPIENT_PHONES = os.getenv("RECIPIENT_PHONES").split(",")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EARTHQUAKE_PARAMS = {
    "format": "geojson",
    "minlatitude": 32.0, # southern limit of California
    "maxlatitude": 52.0, # northern limit of Cascadia
    "minlongitude": -130.0, # western limit
    "maxlongitude": -115.0, # eastern limit
    "minmagnitude": 6.1,
} 

POLL_INTERVAL = 300 # every 5 min
USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def get_recent_earthquakes():
    EARTHQUAKE_PARAMS["starttime"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time() - POLL_INTERVAL))
    EARTHQUAKE_PARAMS["endtime"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

    try:
        response = requests.get(USGS_API_URL, params=EARTHQUAKE_PARAMS)
        data = response.json()
        return data["features"]
    except requests.RequestException as e:
        logger.error(f"Error fetching earthquake data: {e}")
        return []

def send_alert(earthquake):
    formatted_time = _get_formatted_time(earthquake)
    message = f"ALERT! {earthquake['properties']['mag']} magnitude earthquake detected {earthquake['properties']['place']} at {formatted_time}"
    for phone in RECIPIENT_PHONES:
        try:
            client.messages.create(
                body=message,
                from_=TWILIO_PHONE,
                to=phone
            )
            logger.info(f"Sent alert to phone {phone}: {message}")
        except Exception as e:
            logger.error(f"Error sending alert: {e}")

def _get_formatted_time(earthquake):
    utc_time = datetime.fromtimestamp(earthquake['properties']['time'] / 1000, tz=pytz.utc)
    pacific_time = utc_time.astimezone(pytz.timezone('US/Pacific'))
    formatted_time = pacific_time.strftime("%I:%M %p %Z")
    return formatted_time

def monitor():
    while True:
        earthquakes = get_recent_earthquakes()
        for earthquake in earthquakes:
            send_alert(earthquake)
        time.sleep(POLL_INTERVAL)

def main():
    monitor()

if __name__ == "__main__":
    main()
