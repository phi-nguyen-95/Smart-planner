import unittest
from applications.data_analyzer_server.analyzer import calculate_activity_score, get_activity_rating

class TestDataAnalyzer(unittest.TestCase):
    def test_excellent_weather(self):
        score = calculate_activity_score(temperature=22, precipitation=0, wind_speed=10, humidity=50)
        self.assertEqual(score, 100)
    def test_light_rain_reduce_score(self):
        score = calculate_activity_score(temperature=22, precipitation=1, wind_speed=10, humidity=50)
        self.assertEqual(score, 85)
    def test_high_wind_reduce_score(self):
        score = calculate_activity_score(temperature=22, precipitation=0, wind_speed=30, humidity=50)
        self.assertEqual(score, 85)
    def test_bad_weather_score(self):
        score = calculate_activity_score(temperature=38, precipitation=10, wind_speed=45, humidity=95)
        self.assertEqual(score, 0)
    def test_activity_rating(self):
        self.assertEqual(get_activity_rating(90), "Excellent")
        self.assertEqual(get_activity_rating(70), "Good")
        self.assertEqual(get_activity_rating(50), "Fair")
        self.assertEqual(get_activity_rating(30), "Poor")
if __name__ == "__main__":
    unittest.main()
