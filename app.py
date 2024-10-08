from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, date, time
from fastapi import FastAPI, Query
from typing import Annotated

from config import settings
from db import get_forecast_temperature_range, write_forecasts
from nws import get_upcoming_forecasts, write_forecasts

scheduler = BackgroundScheduler()
app = FastAPI()


def fetch_upcoming_forecasts():
    report_time = datetime.utcnow()
    forecasts = get_upcoming_forecasts(report_time)
    write_forecasts(forecasts)

@app.on_event('startup')
def start_scheduler():
    interval = settings.SCHEDULER_INTERVAL_MINUTES
    scheduler.add_job(fetch_upcoming_forecasts, 'interval', minutes=interval)
    scheduler.start()


@app.get('/forecast')
async def get_forecast(
        date: date,
        latitude: float = Query(ge=-90, le=90),
        longitude: float = Query(ge=-180, le=180),
        hour: int = Query(ge=0, le=23)
):
    forecast_datetime = datetime.combine(date, time(hour))
    return get_forecast_temperature_range(latitude, longitude, forecast_datetime)


@app.on_event('shutdown')
def stop_scheduler():
    scheduler.stop()
