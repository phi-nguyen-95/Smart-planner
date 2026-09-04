from sqlalchemy import select
from components.database.database import SessionLocal
from components.database.models import WeatherRecord

def save_weather(weather):
    """
    Save collected weather data to the database.
    """
    record = WeatherRecord(
        location=weather["location"],
        latitude=weather["latitude"],
        longitude=weather["longitude"],
        temperature=weather["temperature"],
        humidity=weather["humidity"],
        precipitation=weather["precipitation"],
        wind_speed=weather["wind_speed"],
        observed_at=weather["observed_at"])
    with SessionLocal() as session:
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
def get_recent_weather(limit=20):
    """
    Return the most recently stored weather records.
    """
    with SessionLocal() as session:
        statement = (select(WeatherRecord).order_by(WeatherRecord.id.desc()).limit(limit))
        records = session.scalars(statement).all()
        return list(records)

def get_recent_weather_by_location(location, limit=2):
    """
    Return the most recent weather records for one specific location.
    """

    with SessionLocal() as session:
        statement = select(WeatherRecord).where(WeatherRecord.location == location).order_by(WeatherRecord.id.desc()).limit(limit)
        records = session.scalars(statement).all()
    return list(records)
