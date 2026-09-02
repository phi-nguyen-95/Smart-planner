from applications.data_collector_server.collector import collect_weather
from applications.data_analyzer_server.analyzer import calculate_activity_score, get_activity_rating

def collect_and_analyze(location):
    """
    Collect weather for a location and analyze whether conditions are suitable for outdoor activities.
    """
    weather = collect_weather(location)
    score = calculate_activity_score(temperature=weather["temperature"],
    precipitation=weather["precipitation"], wind_speed=weather["wind_speed"],
    humidity=weather["humidity"])
    rating = get_activity_rating(score)
    return {"weather": weather, "activity_score": score, "activity_rating": rating}

