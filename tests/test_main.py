import unittest
from unittest.mock import patch, MagicMock
import main
from services.alert_manager import AlertManager
from alerts.earthquake_alert import EarthquakeAlert

class TestMain(unittest.TestCase):
    @patch('services.alert_factory.AlertFactory.create_alert')
    @patch('services.storage_service.StorageService')
    @patch('main.AlertManager')
    def test_lambda_handler(self, MockAlertManager, MockStorageService, mock_create_alert):
        # Mock storage service to return my number
        mock_storage_service_instance = MockStorageService.return_value
        mock_storage_service_instance.get_subscribers.return_value = ['+18102786241']
        mock_storage_service_instance.alert_already_sent.return_value = False

        # Mock alert with 6.5 magnitude earthquake
        mock_alert = MagicMock(spec=EarthquakeAlert)
        mock_alert.fetch_data.return_value = [
            {'properties': {'mag': 6.5, 'place': 'California', 'time': 1623943442000}, 'id': 'test1'}
        ]
        mock_alert.should_alert.return_value = True
        mock_alert.format_alert.return_value = "ALERT! 6.5 magnitude earthquake detected California at 1623943442000"
        mock_create_alert.return_value = mock_alert

        # Initialize the AlertManager with mock storage service but keep actual notification service
        alert_manager = AlertManager(storage_service=mock_storage_service_instance)

        # Patch AlertManager instance to use this half-mocked AlertManager
        MockAlertManager.return_value = alert_manager

        # Run the lambda_handler to trigger the process
        response = main.lambda_handler(None, None)

        # Check the response status code (I should also get a text message!)
        self.assertEqual(response['statusCode'], 200)

if __name__ == '__main__':
    unittest.main()
