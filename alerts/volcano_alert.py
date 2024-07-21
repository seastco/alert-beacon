import requests
from typing import Dict, Any, List, Tuple
from .base_alert import BaseAlert
from config.config import Config
from geopy.geocoders import Nominatim
from geopy.location import Location


class VolcanoAlert(BaseAlert):
    def __init__(self):
        self.config: Config = Config()
        self.api_url: str = "https://volcanoes.usgs.gov/hans-public/api/volcano/getCapElevated"
        self.geolocator: Nominatim = Nominatim(user_agent="catastrophic-alert")

    def fetch_data(self) -> List[Dict[str, Any]]:
        response = requests.get(self.api_url)
        response.raise_for_status()
        return response.json()

    def should_alert(self, volcano: Dict[str, Any]) -> bool:
        required_keys = ["color_code", "alert_level"]
        self._validate_volcano(volcano, required_keys)

        color_code = self.config.get("COLOR_CODE")
        alert_level = self.config.get("ALERT_LEVEL")
        return volcano["color_code"] == color_code and volcano["alert_level"] == alert_level

    def format_alert(self, volcano: Dict[str, Any]) -> str:
        required_keys = ["volcano_name_appended", "latitude", "longitude"]
        self._validate_volcano(volcano, required_keys)

        latitude = volcano["latitude"]
        longitude = volcano["longitude"]
        location = self.geolocator.reverse((latitude, longitude))
        locality, state = self._validate_location(location)
        volcano_name = volcano["volcano_name_appended"]
        return f"ALERT! {volcano_name} near {locality}, {state}, is experiencing a major eruption."

    def get_id(self, volcano: Dict[str, Any]) -> str:
        if "guid" not in volcano:
            raise KeyError("volcano['guid'] does not exist")
        return volcano["guid"]

    def _validate_volcano(self, volcano: Dict[str, Any], required_keys: List[str]) -> None:
        if not isinstance(volcano, dict):
            raise ValueError("invalid volcano object: not a dictionary")
        for key in required_keys:
            if key not in volcano:
                raise KeyError(f"volcano['{key}'] does not exist")

    def _validate_location(self, location: Location) -> Tuple[str, str]:
        address = location.raw.get("address")
        if not address:
            raise KeyError("location address does not exist")

        locality = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("county")
        )
        state = address.get("state")
        if not locality:
            raise KeyError("location address locality does not exist")
        if not state:
            raise KeyError("location address state does not exist")

        return locality, state
