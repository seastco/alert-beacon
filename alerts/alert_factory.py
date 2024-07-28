from typing import Union
from alerts.earthquake_alert import EarthquakeAlert
from alerts.volcano_alert import VolcanoAlert


class AlertFactory:
    @staticmethod
    def create_alert(alert_type: str) -> Union[EarthquakeAlert, VolcanoAlert]:
        if alert_type == "earthquake":
            return EarthquakeAlert()
        if alert_type == "volcano":
            return VolcanoAlert()
        else:
            raise ValueError(f"Unknown alert type: {alert_type}")
