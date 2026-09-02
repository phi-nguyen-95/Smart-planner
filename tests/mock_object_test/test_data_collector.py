import unittest
from unittest.mock import patch, MagicMock
from applications.data_collector_server.collector import collect_weather
class TestDataCollector(unittest.TestCase):
    @patch(
        "applications.data_collector_server.collector.requests.get"
    )
    def test_collect_weather(self, mock_get):
        geo_response = MagicMock()
        geo_response.json.return_value = {"results": [
           {"name": "Montgomery", "admin1": "Alabama", "country": "United States", "latitude": 32.3668, "longitude": -86.3000}]}
        weather_response = MagicMock()
        weather_response.json.return_value = {"current": {
           "time": "2026-09-02T09:00",
           "temperature_2m": 25.0,
           "relative_humidity_2m": 60,
           "precipitation": 0.0,
           "wind_speed_10m": 10.0}}
        mock_get.side_effect = [geo_response, weather_response]
        result = collect_weather("Montgomery, Alabama")
        self.assertEqual(result["location"], "Montgomery, Alabama, United States")
        self.assertEqual(result["temperature"], 25.0)
        self.assertEqual(result["humidity"], 60)
        self.assertEqual(result["precipitation"], 0.0)
        self.assertEqual(result["wind_speed"], 10.0)
        self.assertEqual(mock_get.call_count, 2)
if __name__ == "__main__":
    unittest.main()
