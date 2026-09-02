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
