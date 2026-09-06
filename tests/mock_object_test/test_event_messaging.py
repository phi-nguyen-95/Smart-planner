import json
import unittest
from unittest.mock import MagicMock, patch
from applications.data_collector_server.producer import publish_weather_event
from applications.data_analyzer_server.consumer import callback

class TestEventMessaging(unittest.TestCase):
    @patch("applications.data_collector_server.producer."
           "pika.BlockingConnection")
    def test_producer_publishes_weather_event(self, mock_connection):
        connection =MagicMock()
        channel = MagicMock()
        mock_connection.return_value = connection
        connection.channel.return_value = channel
        weather = {
            "location": "Tukwila, Washington, United States",
            "temperature": 12.5,
            "humidity": 78.0,
            "precipitation": 0.0,
            "wind_speed": 7.1,
            "observed_at": "2026-09-06T16:00"}

        result = publish_weather_event(weather)
        self.assertTrue(result)
        channel.queue_declare.assert_called_once_with(queue="weather_events", durable=True)
        publish_call = channel.basic_publish.call_args
        self.assertEqual(publish_call.kwargs["routing_key"], "weather_events")
        event = json.loads(publish_call.kwargs["body"])
        self.assertEqual(event["event_type"], "weather.collected")
        self.assertEqual(event["weather"]["location"], "Tukwila, Washington, United States")
        connection.close.assert_called_once()
    
    @patch("applications.data_analyzer_server.consumer."
           "process_weather_event")
    def test_consumer_processes_and_acknowledges_event(self, mock_process):
        channel = MagicMock()
        method = MagicMock()
        method.delivery_tag = 123
        weather = {
            "location": "Tukwila, Washington, United States", 
            "temperature": 12.5,
            "humidity": 78.0,
            "precipitattion": 0.0,
            "wind_speed": 7.1}
        event = {"event_type": "weather.collected", "weather": weather}
        body = json.dumps(event).encode("utf-8")
        callback(channel, method, None, body)
        mock_process.assert_called_once_with(weather)
        channel.basic_ack.assert_called_once_with(delivery_tag=123)

if __name__ == "__main__":
    unittest.main()


