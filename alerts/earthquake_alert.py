import requests
from typing import Dict, Any, List
from .base_alert import BaseAlert
from config.config import Config


class EarthquakeAlert(BaseAlert):
    def __init__(self):
        self.config = Config()
        self.api_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    def fetch_data(self) -> List[Dict[str, Any]]:
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

    def should_alert(self, earthquake: Dict[str, Any]) -> bool:
        self._validate_earthquake(earthquake)
        magnitude = earthquake["properties"]["mag"]
        return float(magnitude) >= float(self.config.get("MIN_MAGNITUDE"))

    def format_alert(self, earthquake: Dict[str, Any]) -> str:
        self._validate_earthquake(earthquake)
        magnitude = earthquake["properties"]["mag"]
        place = earthquake["properties"]["place"]
        time = earthquake["properties"]["time"]
        formatted_time = self.config.format_time(time)
        return f"ALERT! {magnitude} magnitude earthquake detected {place} at {formatted_time}"

    def get_id(self, earthquake: Dict[str, Any]) -> str:
        if "id" not in earthquake:
            raise KeyError("earthquake['id'] does not exist")
        return earthquake["id"]

    def _validate_earthquake(self, earthquake: Dict[str, Any]) -> None:
        if not isinstance(earthquake, dict):
            raise ValueError("invalid earthquake object: not a dictionary")

        properties = earthquake.get("properties")
        print(properties)
        if not properties:
            raise KeyError("earthquake['properties'] does not exist")
        if "mag" not in properties:
            raise KeyError("earthquake['properties']['mag'] does not exist")
        if "place" not in properties:
            raise KeyError("earthquake['properties']['place'] does not exist")
        if "time" not in properties:
            raise KeyError("earthquake['properties']['time'] does not exist")
