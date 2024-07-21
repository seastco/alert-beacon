import unittest
from unittest.mock import patch, MagicMock
import main
from services.alert_manager import AlertManager
from alerts.earthquake_alert import EarthquakeAlert
from alerts.volcano_alert import VolcanoAlert


class TestMain(unittest.TestCase):
    @patch("services.alert_factory.AlertFactory.create_alert")
    @patch("services.storage_service.StorageService")
    @patch("main.AlertManager")
    def test_lambda_handler(self, MockAlertManager, MockStorageService, mock_create_alert):
        # Mock storage service to return my number
        mock_storage_service_instance = MockStorageService.return_value
        mock_storage_service_instance.get_subscribers.return_value = ["+18102786241"]
        mock_storage_service_instance.alert_already_sent.return_value = False

        # Mock EarthquakeAlert
        mock_earthquake_alert = MagicMock(spec=EarthquakeAlert)
        mock_earthquake_alert.fetch_data.return_value = [
            {
                "properties": {
                    "mag": 6.5,
                    "place": "California",
                    "time": 1623943442000,
                },
                "id": "test1",
            }
        ]
        mock_earthquake_alert.should_alert.return_value = True
        mock_earthquake_alert.format_alert.return_value = (
            "ALERT! 6.5 magnitude earthquake detected California at 1623943442000"
        )

        # Mock VolcanoAlert
        mock_volcano_alert = MagicMock(spec=VolcanoAlert)
        mock_volcano_alert.fetch_data.return_value = [
            {
                "volcano_name_appended": "Mount Example",
                "latitude": 10.0,
                "longitude": 20.0,
                "color_code": "RED",
                "alert_level": "WARNING",
            }
        ]
        mock_volcano_alert.should_alert.return_value = True
        mock_volcano_alert.format_alert.return_value = "RED ALERT! A major volcanic eruption of Mount Example is underway near Locality, State."

        # Adjust mock_create_alert to return appropriate mock based on alert type
        def side_effect(alert_type):
            if alert_type == "earthquake":
                return mock_earthquake_alert
            elif alert_type == "volcano":
                return mock_volcano_alert
            else:
                raise ValueError(f"Unknown alert type: {alert_type}")

        mock_create_alert.side_effect = side_effect

        # Initialize the AlertManager with mock storage service but keep actual notification service
        alert_manager = AlertManager(storage_service=mock_storage_service_instance)

        # Patch AlertManager instance to use this half-mocked AlertManager
        MockAlertManager.return_value = alert_manager

        # Run the lambda_handler to trigger the process
        response = main.lambda_handler(None, None)

        # Check the response status code (I should also get a text message!)
        self.assertEqual(response["statusCode"], 200)


if __name__ == "__main__":
    unittest.main()
