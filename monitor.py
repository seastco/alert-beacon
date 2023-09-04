import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

POLL_INTERVAL = 180 # every 3 minutes

EARTHQUAKE_PARAMS = {
    "format": "geojson",
    "minlatitude": 32.0, # southern limit of California
    "maxlatitude": 52.0, # northern limit of Cascadia
    "minlongitude": -130.0, # western limit
    "maxlongitude": -115.0, # eastern limit
    "minmagnitude": 6.0,
} 

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
    try:
        message = f"ALERT! Earthquake detected: Magnitude {earthquake['properties']['mag']} at {earthquake['properties']['place']}"
        print(message)
        # TODO: twilio integration
        logger.info(f"Sent alert for earthquake: {message}")
    except Exception as e:
        logger.error(f"Error sending alert: {e}")

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
