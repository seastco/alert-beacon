import requests
from typing import Dict, Any, List
from .base_alert import BaseAlert
from config.config import Config


class EarthquakeAlert(BaseAlert):
    def __init__(self):
        self.config: Config = Config()
        self.api_url: str = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        self.regions = [
            {
                "name": "Continental US",
                "minmagnitude": self.config.get("CONUS_MIN_MAGNITUDE"),
                "minlatitude": self.config.get("CONUS_MIN_LATITUDE"),
                "maxlatitude": self.config.get("CONUS_MAX_LATITUDE"),
                "minlongitude": self.config.get("CONUS_MIN_LONGITUDE"),
                "maxlongitude": self.config.get("CONUS_MAX_LONGITUDE"),
            },
            {
                "name": "Alaska",
                "minmagnitude": self.config.get("ALASKA_MIN_MAGNITUDE"),
                "minlatitude": self.config.get("ALASKA_MIN_LATITUDE"),
                "maxlatitude": self.config.get("ALASKA_MAX_LATITUDE"),
                "minlongitude": self.config.get("ALASKA_MIN_LONGITUDE"),
                "maxlongitude": self.config.get("ALASKA_MAX_LONGITUDE"),
            },
            {
                "name": "Hawaii",
                "minmagnitude": self.config.get("HAWAII_MIN_MAGNITUDE"),
                "minlatitude": self.config.get("HAWAII_MIN_LATITUDE"),
                "maxlatitude": self.config.get("HAWAII_MAX_LATITUDE"),
                "minlongitude": self.config.get("HAWAII_MIN_LONGITUDE"),
                "maxlongitude": self.config.get("HAWAII_MAX_LONGITUDE"),
            },
        ]

    def fetch_data(self) -> List[Dict[str, Any]]:
        data = []

        for region in self.regions:
            params = {
                "format": "geojson",
                "starttime": self.config.get_start_time(),
                "endtime": self.config.get_current_time(),
                "minmagnitude": region["minmagnitude"],
                "minlatitude": region["minlatitude"],
                "maxlatitude": region["maxlatitude"],
                "minlongitude": region["minlongitude"],
                "maxlongitude": region["maxlongitude"],
            }
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            region_data = response.json().get("features", [])
            data.extend(region_data)

        return data

    def should_alert(self, earthquake: Dict[str, Any]) -> bool:
        # fetch_data does all the necessary filtering
        return True

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
        if not properties:
            raise KeyError("earthquake['properties'] does not exist")
        if "mag" not in properties:
            raise KeyError("earthquake['properties']['mag'] does not exist")
        if "place" not in properties:
            raise KeyError("earthquake['properties']['place'] does not exist")
        if "time" not in properties:
            raise KeyError("earthquake['properties']['time'] does not exist")
