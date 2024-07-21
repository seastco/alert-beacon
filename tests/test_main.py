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
        # Set up mock storage service
        mock_storage_service = MockStorageService.return_value
        mock_storage_service.get_subscribers.return_value = ["+18102786241"]
        mock_storage_service.alert_already_sent.return_value = False

        # Set up mock alerts
        mock_alerts = {
            "earthquake": self._create_mock_earthquake_alert(),
            "volcano": self._create_mock_volcano_alert(),
        }

        # Set up mock create_alert function
        mock_create_alert.side_effect = lambda alert_type: mock_alerts[alert_type]

        # Initialize and patch AlertManager
        alert_manager = AlertManager(storage_service=mock_storage_service)
        MockAlertManager.return_value = alert_manager

        # Run the lambda_handler
        response = main.lambda_handler(None, None)
        self.assertEqual(response["statusCode"], 200)

    @staticmethod
    def _create_mock_earthquake_alert():
        mock_alert = MagicMock(spec=EarthquakeAlert)
        mock_alert.fetch_data.return_value = [
            {
                "properties": {
                    "mag": 6.5,
                    "place": "219 km WSW of Tofino, Canada",
                    "time": "8:08 AM PDT",
                },
                "id": "test1",
            }
        ]
        mock_alert.should_alert.return_value = True
        mock_alert.format_alert.return_value = (
            "ALERT! 6.5 magnitude earthquake detected 219 km WSW of Tofino, Canada at 8:08 AM PDT"
        )
        return mock_alert

    @staticmethod
    def _create_mock_volcano_alert():
        mock_alert = MagicMock(spec=VolcanoAlert)
        mock_alert.fetch_data.return_value = [
            {
                "volcano_name_appended": "Mount Vesuvius",
                "latitude": 10.0,
                "longitude": 20.0,
                "color_code": "RED",
                "alert_level": "WARNING",
            }
        ]
        mock_alert.should_alert.return_value = True
        mock_alert.format_alert.return_value = (
            "ALERT! Mount Vesuvius near Locality, State, is experiencing a major eruption."
        )
        return mock_alert


if __name__ == "__main__":
    unittest.main()
