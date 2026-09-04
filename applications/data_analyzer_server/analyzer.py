def calculate_activity_score(temperature, precipitation, wind_speed, humidity):
    """
    Calculate an outdoor activity suitability score from 0 to 100.
    """
    score = 100
    if temperature < 5 or temperature > 35:
        score -= 30
    elif temperature < 10 or temperature >30:
        score -= 20
    if precipitation >= 5:
        score -=30
    elif precipitation > 0:
        score -=15
    if wind_speed >=40:
        score -= 30
    elif wind_speed >= 25:
        score -= 15
    if humidity >= 90:
        score -= 10
    return max(0,min(100, score))

def get_activity_rating(score):
    """
    Convert the numeric activity score into a human-reachable rating.
    """
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Fair"
    else:
        return "Poor"

def analyze_weather_trend(current, previous):
    """
    Compare two weather records and determine whether outdoor conditions
    are improving, worsening, or stable.
    """
    temperature_change = round(current.temperature-previous.temperature,1)   
    humidity_change = round(current.humidity-previous.humidity,1)
    precipitation_change = round(current.precipitation-previous.precipitation,1)
    wind_change = round(current.wind_speed-previous.wind_speed,1)
    current_score = calculate_activity_score(current.temperature,
    current.precipitation, current.wind_speed, current.humidity)
    previous_score = calculate_activity_score(previous.temperature,
    previous.precipitation, previous.wind_speed, previous.humidity)
    score_change = current_score-previous_score
    if score_change >= 5:
        overall_trend = "Improving"
    elif score_change <= -5:
        ovarall_trend = "Worsening"
    else:
        overall_trend = "Stable"
    return {
        "temperature_change": temperature_change,
        "humidity_change": humidity_change,
        "precipitation_change": precipitation_change,
        "wind_change": wind_change,
        "previous_activity_score": previous_score,
        "current_activity_score": current_score,
        "activity_score_change": score_change,
        "overall_trend": overall_trend }
   
