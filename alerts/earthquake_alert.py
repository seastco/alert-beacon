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
            "minmagnitude": self.config.get('MIN_MAGNITUDE'),
            "minlatitude": self.config.get('MIN_LATITUDE'),
            "maxlatitude": self.config.get('MAX_LATITUDE'),
            "minlongitude": self.config.get('MIN_LONGITUDE'),
            "maxlongitude": self.config.get('MAX_LONGITUDE'),
        }
        response = requests.get(self.api_url, params=params)
        return response.json().get("features", [])

    def should_alert(self, earthquake):
        return float(earthquake['properties']['mag']) >= float(self.config.get('MIN_MAGNITUDE'))

    def format_alert(self, earthquake):
        return f"ALERT! {earthquake['properties']['mag']} magnitude earthquake detected {earthquake['properties']['place']} at {self.config.format_time(earthquake['properties']['time'])}"
