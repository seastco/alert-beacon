from alerts.earthquake_alert import EarthquakeAlert


class AlertFactory:
    @staticmethod
    def create_alert(alert_type):
        if alert_type == "earthquake":
            return EarthquakeAlert()
        else:
            raise ValueError(f"Unknown alert type: {alert_type}")
