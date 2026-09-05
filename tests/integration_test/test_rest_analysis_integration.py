import threading
import unittest

from sqlalchemy import delete
from werkzeug.serving import make_server
import components.analysis_client as analysis_client
from applications.data_analyzer_server.app import app as analyzer_app
from components.database.database import SessionLocal, init_db
from components.database.models import WeatherRecord
from components.database.repository import save_weather

class TestRestAnalysisIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Start the real Data Analyzer Flask service on an available local port.
        """
        init_db()
        cls.server = make_server("127.0.0.1", 0, analyzer_app)
        cls.port = cls.server.server_port
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.original_analyzer_url = analysis_client.ANALYZER_BASE_URL
        analysis_client.ANALYZER_BASE_URL = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        """
        Stop the temporary REST service.
        """
        analysis_client.ANALYZER_BASE_URL = cls.original_analyzer_url
        cls.server.shutdown()
        cls.server_thread.join()

    def setUp(self):
        """
        Insert database records before each test.
        """
        self.location = "REST Integration Test City"
        self._delete_test_records()
	# Bad weather record        
        save_weather({"location": self.location, "latitude": 47.0, "longitude": -122.0,
        "temperature": 38.0, "humidity": 95.0, "precipitation": 10.0,
        "wind_speed": 45.0, "observed_at": "2026-09-04T10:00"})
        # Good weather record
        save_weather({"location": self.location, "latitude": 47.0, "longitude": -122.0,
        "temperature": 22.0, "humidity": 50.0, "precipitation": 0.0,
        "wind_speed": 10.0, "observed_at": "2026-09-04T11:00"})
        
    def tearDown(self):
        """
        Remove test records so the test does not pollute normal Weather History.
        """
        self._delete_test_records()

    def _delete_test_records(self):
        with SessionLocal() as session:
            session.execute(delete(WeatherRecord).where(WeatherRecord.location == "REST Integration Test City"))
        session.commit()

    def test_rest_trend_colloboration(self):
        """
        Verify that the analysis client communicates with the real analyzer REST service.
        """
        result = analysis_client.get_trend_analysis(self.location)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["location"], self.location)
        self.assertEqual(result["overall_trend"], "Improving")
        self.assertGreater(result["activity_score_change"], 0)

if __name__ == "__main__":
    unittest.main()
