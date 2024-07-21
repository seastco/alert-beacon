import unittest
from unittest.mock import patch
from alerts.earthquake_alert import EarthquakeAlert

class TestEarthquakeAlert(unittest.TestCase):
    @patch('alerts.earthquake_alert.requests.get')
    def test_fetch_data(self, mock_get):
        mock_response = {
            "features": [
                {"properties": {"mag": 5.0, "place": "California", "time": 1623943442000}, "id": "test1"},
                {"properties": {"mag": 4.0, "place": "Nevada", "time": 1623943442000}, "id": "test2"},
            ]
        }
        mock_get.return_value.json.return_value = mock_response

        alert = EarthquakeAlert()
        data = alert.fetch_data()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['properties']['place'], "California")

    def test_should_alert(self):
        alert = EarthquakeAlert()
        earthquake = {"properties": {"mag": 6.5}}
        self.assertTrue(alert.should_alert(earthquake))

    def test_format_alert(self):
        alert = EarthquakeAlert()
        earthquake = {"properties": {"mag": 6.5, "place": "California", "time": 1623943442000}}
        formatted_alert = alert.format_alert(earthquake)
        self.assertIn("ALERT!", formatted_alert)
        self.assertIn("6.5 magnitude earthquake detected California", formatted_alert)

if __name__ == '__main__':
    unittest.main()
