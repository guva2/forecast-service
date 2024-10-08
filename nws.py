import pytz
import requests

from datetime import datetime
from dateutil.parser import parse

from config import settings
from db import Forecast, write_forecasts

import logging

logger = logging.getLogger(__name__)

LOOKAHEAD_HOURS: int = 72

def get_upcoming_forecasts(report_time: datetime):
    api_base = settings.NWS_API_BASE
    latitude = settings.FORECAST_LATITUDE
    longitude = settings.FORECAST_LONGITUDE

    logger.info(f'Fetching forecasts for {latitude}, {longitude}')

    points_uri = f'{api_base}/points/{latitude},{longitude}'
    point = requests.get(points_uri).json()
    hourly_forecast_uri = point.get('properties', {}).get('forecastHourly')
    if not hourly_forecast_uri:
        return []

    forecast = requests.get(hourly_forecast_uri).json()
    periods = forecast.get('properties', {}).get('periods')
    if not periods:
        return []

    return [build_forecast(period, report_time) for period in periods[:LOOKAHEAD_HOURS]]


def build_forecast(period: dict, report_time: datetime):
    return {
        'forecast_time': parse(period['startTime']).astimezone(pytz.utc),
        'report_time': report_time.astimezone(pytz.utc),
        'temperature': period['temperature']
    }

        

