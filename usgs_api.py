import os
import requests
import time
import logging

logger = logging.getLogger(__name__)

MIN_MAGNITUDE = float(os.getenv('MIN_MAGNITUDE', '6.1'))
MIN_LATITUDE = float(os.getenv('MIN_LATITUDE', '32.0'))
MAX_LATITUDE = float(os.getenv('MAX_LATITUDE', '52.0'))
MIN_LONGITUDE = float(os.getenv('MIN_LONGITUDE', '-130.0'))
MAX_LONGITUDE = float(os.getenv('MAX_LONGITUDE', '-115.0'))
SECONDS_IN_PAST = int(os.getenv('SECONDS_IN_PAST', '601'))
USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

EARTHQUAKE_PARAMS = {
    "format": "geojson",
    "minlatitude": MIN_LATITUDE,  # southern limit of California
    "maxlatitude": MAX_LATITUDE,  # northern limit of Cascadia
    "minlongitude": MIN_LONGITUDE,  # western limit
    "maxlongitude": MAX_LONGITUDE,  # eastern limit
    "minmagnitude": MIN_MAGNITUDE,
}

def get_recent_earthquakes():
    EARTHQUAKE_PARAMS["starttime"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time() - SECONDS_IN_PAST))
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
