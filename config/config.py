import os
import pytz
import time
from datetime import datetime
from typing import Dict


class Config:
    def __init__(self):
        self.config: Dict[str, str] = {
            "CONUS_MIN_MAGNITUDE": os.getenv("CONUS_MIN_MAGNITUDE", "6.5"),
            "CONUS_MIN_LATITUDE": os.getenv("CONUS_MIN_LATITUDE", "24.396308"),
            "CONUS_MAX_LATITUDE": os.getenv("CONUS_MAX_LATITUDE", "51.500000"),
            "CONUS_MIN_LONGITUDE": os.getenv("CONUS_MIN_LONGITUDE", "-130.000000"),
            "CONUS_MAX_LONGITUDE": os.getenv("CONUS_MAX_LONGITUDE", "-66.934570"),
            "ALASKA_MIN_MAGNITUDE": os.getenv("ALASKA_MIN_MAGNITUDE", "7.0"),
            "ALASKA_MIN_LATITUDE": os.getenv("ALASKA_MIN_LATITUDE", "56.500000"),
            "ALASKA_MAX_LATITUDE": os.getenv("ALASKA_MAX_LATITUDE", "71.500000"),
            "ALASKA_MIN_LONGITUDE": os.getenv("ALASKA_MIN_LONGITUDE", "-169.000000"),
            "ALASKA_MAX_LONGITUDE": os.getenv("ALASKA_MAX_LONGITUDE", "-140.000000"),
            "HAWAII_MIN_MAGNITUDE": os.getenv("HAWAII_MIN_MAGNITUDE", "7.0"),
            "HAWAII_MIN_LATITUDE": os.getenv("HAWAII_MIN_LATITUDE", "18.000000"),
            "HAWAII_MAX_LATITUDE": os.getenv("HAWAII_MAX_LATITUDE", "22.750000"),
            "HAWAII_MIN_LONGITUDE": os.getenv("HAWAII_MIN_LONGITUDE", "-160.750000"),
            "HAWAII_MAX_LONGITUDE": os.getenv("HAWAII_MAX_LONGITUDE", "-154.000000"),
            "VOLCANIC_COLOR_CODE": os.getenv("VOLCANIC_COLOR_CODE", "RED"),
            "VOLCANIC_ALERT_LEVEL": os.getenv("VOLCANIC_ALERT_LEVEL", "WARNING"),
            "SECONDS_IN_PAST": os.getenv("SECONDS_IN_PAST", "601"),
            "ENVIRONMENT": os.getenv("ENVIRONMENT", "prod"),
            "TEST_SUBSCRIBERS": os.getenv("TEST_SUBSCRIBERS", "").split(","),
        }

    def get(self, key: str) -> str:
        return self.config.get(key, "")

    def get_start_time(self) -> str:
        return time.strftime(
            "%Y-%m-%dT%H:%M:%S",
            time.gmtime(time.time() - int(self.config["SECONDS_IN_PAST"])),
        )

    def get_current_time(self) -> str:
        return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

    @staticmethod
    def format_time(timestamp: int) -> str:
        utc_time = datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc)
        pacific_time = utc_time.astimezone(pytz.timezone("US/Pacific"))
        return pacific_time.strftime("%-I:%M %p %Z")
