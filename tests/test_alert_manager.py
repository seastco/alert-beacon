import unittest
from unittest.mock import MagicMock, patch
from services.alert_manager import AlertManager
from alerts.earthquake_alert import EarthquakeAlert


class TestAlertManager(unittest.TestCase):
    @patch("services.alert_manager.StorageService")
    @patch("services.alert_manager.NotificationService")
    @patch("services.alert_factory.AlertFactory.create_alert")
    def test_process_alerts(
        self, mock_create_alert, MockNotificationService, MockStorageService
    ):
        # Mock storage service
        mock_storage_service = MockStorageService.return_value
        mock_storage_service.get_subscribers.return_value = [
            "+1234567890",
            "+0987654321",
        ]
        mock_storage_service.alert_already_sent.return_value = False

        # Mock notification service
        mock_notification_service = MockNotificationService.return_value

        # Mock alert
        mock_alert = MagicMock(spec=EarthquakeAlert)
        mock_alert.fetch_data.return_value = [
            {
                "properties": {
                    "mag": 6.5,
                    "place": "California",
                    "time": 1623943442000,
                },
                "id": "test1",
            },
            {
                "properties": {"mag": 4.0, "place": "Nevada", "time": 1623943442000},
                "id": "test2",
            },
        ]
        mock_alert.should_alert.side_effect = (
            lambda item: item["properties"]["mag"] >= 6.0
        )
        mock_alert.format_alert.side_effect = (
            lambda item: f"ALERT! {item['properties']['mag']} magnitude earthquake detected {item['properties']['place']} at {item['properties']['time']}"
        )
        mock_create_alert.return_value = mock_alert

        # Initialize AlertManager with mocks
        alert_manager = AlertManager(
            notification_service=mock_notification_service,
            storage_service=mock_storage_service,
        )

        # Process alerts
        alert_manager.process_alerts(["earthquake"])

        # Verify that send_alert and store_sent_alert were called the expected number of times
        expected_message = (
            "ALERT! 6.5 magnitude earthquake detected California at 1623943442000"
        )
        mock_notification_service.send_alert.assert_called_with(
            expected_message, ["+1234567890", "+0987654321"]
        )
        mock_storage_service.store_sent_alert.assert_called_once_with("test1")


if __name__ == "__main__":
    unittest.main()
