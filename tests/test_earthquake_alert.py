import unittest
from unittest.mock import patch
from alerts.earthquake_alert import EarthquakeAlert


class TestEarthquakeAlert(unittest.TestCase):
    def setUp(self):
        self.alert = EarthquakeAlert()

    @patch("alerts.earthquake_alert.requests.get")
    def test_fetch_data(self, mock_get):
        mock_responses = [
            {
                "features": [
                    {
                        "properties": {
                            "mag": 5.0,
                            "place": "6 km NW of Tofino, Canada",
                            "time": "8:08 AM PDT",
                        },
                        "id": "test1",
                    }
                ]
            },
            {
                "features": [
                    {
                        "properties": {
                            "mag": 4.0,
                            "place": "4 km SW of Las Vegas, Nevada",
                            "time": "8:08 AM PDT",
                        },
                        "id": "test2",
                    }
                ]
            },
            {"features": []},
        ]

        def side_effect(url, params):
            if params["minlatitude"] == self.alert.regions[0]["minlatitude"]:
                return MockResponse(mock_responses[0])
            elif params["minlatitude"] == self.alert.regions[1]["minlatitude"]:
                return MockResponse(mock_responses[1])
            else:
                return MockResponse(mock_responses[2])

        mock_get.side_effect = side_effect

        data = self.alert.fetch_data()

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["properties"]["place"], "6 km NW of Tofino, Canada")
        self.assertEqual(data[1]["properties"]["place"], "4 km SW of Las Vegas, Nevada")

    def test_should_alert(self):
        earthquake = {"properties": {"mag": 6.5, "place": "California", "time": 1623943442000}}
        self.assertTrue(self.alert.should_alert(earthquake))

    def test_format_alert(self):
        earthquake = {
            "properties": {
                "mag": 6.5,
                "place": "5 km NE of Detroit, Michigan",
                "time": 1623943442000,
            }
        }
        formatted_alert = self.alert.format_alert(earthquake)
        self.assertIn("ALERT!", formatted_alert)
        self.assertIn(
            "6.5 magnitude earthquake detected 5 km NE of Detroit, Michigan",
            formatted_alert,
        )


class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data

    def raise_for_status(self):
        pass


if __name__ == "__main__":
    unittest.main()
