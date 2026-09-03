from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT/"weather.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def init_db():
    """
    Create all database tables if they do not already exist.
    """
    from components.database.models import WeatherRecord
    Base.metadata.create_all(bind=engine)
