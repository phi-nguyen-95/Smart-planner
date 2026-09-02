import unittest
from unittest.mock import patch, MagicMock
from components.weather_pipeline import collect_and_analyze

class TestCollectorAnalyzerIntegration(unittest.TestCase):
    @patch(
        "applications.data_collector_server.collector.requests.get"
    )
    def test_collector_analyzer_integration(self, mock_get):
        geo_response = MagicMock()
        geo_response.json.return_value = {
            "results": [
                {
                    "name": "Montgomery",
                    "admin1": "Alabama",
                    "country": "United States",
                    "latitude": 32.3668,
                    "longitude": -86.3000,
                }
            ]
        }

        weather_response = MagicMock()
        weather_response.json.return_value = {
            "current": {
                "time": "2026-09-02T10:00",
                "temperature_2m": 25.0,
                "relative_humidity_2m": 60,
                "precipitation": 0.0,
                "wind_speed_10m": 10.0,
            }
        }

        mock_get.side_effect = [geo_response, weather_response]
        result = collect_and_analyze("Montgomery, Alabama")

        # verify data collector output
        self.assertEqual(result["weather"]["location"], "Montgomery, Alabama, United States")
        self.assertEqual(result["weather"]["temperature"], 25.0)

        # verify data analyzer output
        self.assertEqual(result["activity_score"], 100)
        self.assertEqual(result["activity_rating"], "Excellent")
if __name__ == "__main__":
    unittest.main()

