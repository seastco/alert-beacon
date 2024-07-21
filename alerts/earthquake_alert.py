import requests
from .base_alert import BaseAlert
from config.config import Config


class EarthquakeAlert(BaseAlert):
    def __init__(self):
        self.config = Config()
        self.api_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    def fetch_data(self):
        params = {
            "format": "geojson",
            "starttime": self.config.get_start_time(),
            "endtime": self.config.get_current_time(),
            "minmagnitude": self.config.get("MIN_MAGNITUDE"),
            "minlatitude": self.config.get("MIN_LATITUDE"),
            "maxlatitude": self.config.get("MAX_LATITUDE"),
            "minlongitude": self.config.get("MIN_LONGITUDE"),
            "maxlongitude": self.config.get("MAX_LONGITUDE"),
        }
        response = requests.get(self.api_url, params=params)
        response.raise_for_status()
        return response.json().get("features", [])

    def should_alert(self, earthquake):
        if not isinstance(earthquake, dict):
            raise ValueError("invalid earthquake object: not a dictionary")

        properties = earthquake.get("properties")
        if not properties:
            raise KeyError("earthquake['properties'] does not exist")

        magnitude = properties.get("mag")
        if not magnitude:
            raise KeyError("earthquake['properties']['mag'] does not exist")

        return float(magnitude) >= float(self.config.get("MIN_MAGNITUDE"))

    def format_alert(self, earthquake):
        if not isinstance(earthquake, dict):
            raise ValueError("invalid earthquake object: not a dictionary")

        properties = earthquake.get("properties")
        if not properties:
            raise KeyError("earthquake['properties'] does not exist")

        magnitude = properties.get("mag")
        place = properties.get("place")
        time = properties.get("time")
        if not magnitude:
            raise KeyError("earthquake['properties']['mag'] does not exist")
        if not place:
            raise KeyError("earthquake['properties']['place'] does not exist")
        if not time:
            raise KeyError("earthquake['properties']['time'] does not exist")

        formatted_time = self.config.format_time(time)
        return f"ALERT! {magnitude} magnitude earthquake detected {place} at {formatted_time}"
