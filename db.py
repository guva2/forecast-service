from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import func

from config import settings
from datetime import datetime


# Set up database
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Declare database models
class Forecast(Base):
    __tablename__ = "forecast"

    id = Column(Integer, primary_key=True)
    forecast_time = Column(DateTime, index=True)
    report_time = Column(DateTime)
    temperature = Column(Integer, index=True)


# Complete db and table set up
Base.metadata.create_all(engine)


# DB read and write operations
def get_forecast_temperature_range(latitude: float, longitude: float, forecast_time: datetime):
    with Session(engine) as session:
        result = session.query(
                func.min(Forecast.temperature), 
                func.max(Forecast.temperature)
        ).filter(Forecast.forecast_time==forecast_time)

        if result:
            (min_forecast_temperature, max_forecast_temperature) = result[0] 
            return { 
                'min_forecast_temperature': min_forecast_temperature, 
                'max_forecast_temperature': max_forecast_temperature
            } 
        return {}


def write_forecasts(forecasts: list[Forecast]):
    with Session(engine) as session:
        for forecast in forecasts:
            session.add(Forecast(**forecast))
        session.commit()
