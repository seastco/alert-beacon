import os
import pytz
import time
from datetime import datetime
from typing import Dict


class Config:
    def __init__(self):
        self.config: Dict[str, str] = {
            "MIN_MAGNITUDE": os.getenv("MIN_MAGNITUDE", "6.1"),
            "MIN_LATITUDE": os.getenv("MIN_LATITUDE", "32.0"),
            "MAX_LATITUDE": os.getenv("MAX_LATITUDE", "52.0"),
            "MIN_LONGITUDE": os.getenv("MIN_LONGITUDE", "-130.0"),
            "MAX_LONGITUDE": os.getenv("MAX_LONGITUDE", "-115.0"),
            "SECONDS_IN_PAST": os.getenv("SECONDS_IN_PAST", "601"),
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
        return pacific_time.strftime("%I:%M %p %Z")
