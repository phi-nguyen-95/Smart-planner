import unittest
from applications.basic_server.app import app

class TestMonitoringEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["service"],"smart-planner-basic-server")

    def test_metrics_endpoint(self):
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("requests_total", data)
        self.assertIn("errors_total", data)
        self.assertIn("request_per_second", data)
        self.assertIn("uptime_seconds", data)
        self.assertGreaterEqual(data["requests_total"], 1)       
        self.assertGreaterEqual(data["request_per_second"], 0)

if __name__ == "__main__":
    unittest.main()


