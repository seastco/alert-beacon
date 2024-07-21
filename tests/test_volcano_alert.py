import unittest
from unittest.mock import patch, MagicMock
from alerts.volcano_alert import VolcanoAlert


class TestVolcanoAlert(unittest.TestCase):
    def setUp(self):
        self.alert = VolcanoAlert()

    @patch("alerts.volcano_alert.requests.get")
    def test_fetch_data(self, mock_get):
        mock_response = [
            {
                "volcano_name_appended": "Mount Vesuvius",
                "color_code": "RED",
                "alert_level": "WARNING",
                "latitude": "40.821",
                "longitude": "14.426",
                "guid": "test1",
            },
            {
                "volcano_name_appended": "Mount Etna",
                "color_code": "ORANGE",
                "alert_level": "WATCH",
                "latitude": "37.748",
                "longitude": "14.999",
                "guid": "test2",
            },
        ]
        mock_get.return_value.json.return_value = mock_response

        data = self.alert.fetch_data()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["volcano_name_appended"], "Mount Vesuvius")

    def test_should_alert(self):
        volcano = {"color_code": "RED", "alert_level": "WARNING"}
        self.assertTrue(self.alert.should_alert(volcano))

    def test_format_alert(self):
        # Create a mock for the geolocator
        mock_geolocator = MagicMock()
        mock_location = MagicMock()
        mock_location.raw = {"address": {"town": "Ottaviano", "state": "Campania"}}
        mock_geolocator.reverse.return_value = mock_location
        self.alert.geolocator = mock_geolocator

        volcano = {
            "volcano_name_appended": "Mount Vesuvius",
            "latitude": "40.821",
            "longitude": "14.426",
        }
        formatted_alert = self.alert.format_alert(volcano)

        # Check that the geolocator was called with the correct coordinates
        mock_geolocator.reverse.assert_called_once_with(("40.821", "14.426"))

        # Assert the content of the formatted alert
        expected_alert = (
            "ALERT! Mount Vesuvius near Ottaviano, Campania, is experiencing a major eruption."
        )
        self.assertEqual(formatted_alert, expected_alert)


if __name__ == "__main__":
    unittest.main()
