import unittest
from applications.data_analyzer_server.analyzer import calculate_activity_score, get_activity_rating, analyze_weather_trend

from types import SimpleNamespace

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

    def test_weather_trend_stable(self):
        previous = SimpleNamespace(
            temperature=12.8,
            humidity=88.0,
            precipitation=0.0,
            wind_speed=4.0,
        )

        current = SimpleNamespace(
            temperature=12.6,
            humidity=87.0,
            precipitation=0.0,
            wind_speed=5.8,
        )

        result = analyze_weather_trend(
            current=current,
            previous=previous,
        )

        self.assertEqual(result["overall_trend"], "Stable")
        self.assertEqual(result["temperature_change"], -0.2)
        self.assertEqual(result["humidity_change"], -1.0)
        self.assertEqual(result["wind_change"], 1.8)
        self.assertEqual(result["activity_score_change"], 0)

    def test_weather_trend_improving(self):
        previous = SimpleNamespace(
            temperature=38.0,
            humidity=95.0,
            precipitation=10.0,
            wind_speed=45.0,
        )

        current = SimpleNamespace(
            temperature=22.0,
            humidity=50.0,
            precipitation=0.0,
            wind_speed=10.0,
        )

        result = analyze_weather_trend(
            current=current,
            previous=previous,
        )

        self.assertEqual(result["overall_trend"], "Improving")
        self.assertGreater(
             result["activity_score_change"], 0)

if __name__ == "__main__":
    unittest.main()
