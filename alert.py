import os
import requests
import time
import logging
import pytz
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Twilio configuration
TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE = os.environ["TWILIO_PHONE"]
RECIPIENT_PHONES = os.environ["RECIPIENT_PHONES"].split(",")

EARTHQUAKE_PARAMS = {
    "format": "geojson",
    "minlatitude": 32.0, # southern limit of California
    "maxlatitude": 52.0, # northern limit of Cascadia
    "minlongitude": -130.0, # western limit
    "maxlongitude": -115.0, # eastern limit
    "minmagnitude": 6.1,
} 

POLL_INTERVAL = 180 # every 3 min
USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def get_recent_earthquakes():
    EARTHQUAKE_PARAMS["starttime"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time() - POLL_INTERVAL))
    EARTHQUAKE_PARAMS["endtime"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

    try:
        response = requests.get(USGS_API_URL, params=EARTHQUAKE_PARAMS)
        response.raise_for_status()
        data = response.json()
        return data.get("features", [])
    except requests.RequestException as e:
        logger.error(f"Error fetching earthquake data: {e}")
    except ValueError as e:  # Catch JSONDecodeError
        logger.error(f"Unable to decode JSON response: {e}")
    except Exception as e:  # Catch any other exception
        logger.error(f"An unexpected error occurred: {e}")
    
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

def main():
    while True:
        earthquakes = get_recent_earthquakes()
        for earthquake in earthquakes:
            send_alert(earthquake)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()

