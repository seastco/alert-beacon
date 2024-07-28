import unittest
import alerts.handler as handler
from alerts.alert_manager import AlertManager
from alerts.earthquake_alert import EarthquakeAlert
from alerts.volcano_alert import VolcanoAlert
from unittest.mock import patch, MagicMock


class TestMain(unittest.TestCase):
    @patch("alerts.alert_factory.AlertFactory.create_alert")
    @patch("storage.alerts.SentAlerts")
    @patch("storage.subscribers.Subscribers")
    @patch("alerts.handler.AlertManager")
    def test_lambda_handler(
        self, MockAlertManager, MockSubscribers, MockSentAlerts, mock_create_alert
    ):
        # Set up storage mocks
        mock_sent_alerts = MockSentAlerts.return_value
        mock_subscribers = MockSubscribers.return_value
        mock_subscribers.get_subscribers.return_value = ["+18102786241"]
        mock_sent_alerts.alert_already_sent.return_value = False

        # Set up mock alerts
        mock_alerts = {
            "earthquake": self._create_mock_earthquake_alert(),
            "volcano": self._create_mock_volcano_alert(),
        }

        # Set up mock create_alert function
        mock_create_alert.side_effect = lambda alert_type: mock_alerts[alert_type]

        # Initialize and patch AlertManager
        alert_manager = AlertManager(
            sent_alerts_table=mock_sent_alerts, subscribers_table=mock_subscribers
        )
        MockAlertManager.return_value = alert_manager

        # Run the lambda_handler
        response = handler.lambda_handler(None, None)
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
