import os

import requests
from celery import shared_task
from celery.utils.log import get_task_logger

from config import RATES_API_URL
from converter.models import CurrencyConverter
from converter.serializers import CurrencyConverterSerializer

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("Starting sample_task")
    api_data = get_rates_api()
    logger.info(f"Received API data: {api_data}")
    converted_data = covert_info(api_data)
    logger.info(f"Converted data: {converted_data}")

    if not CurrencyConverter.objects.filter(currency="USD").exists():
        CurrencyConverter.objects.create(currency="USD", cur_to_usd=1)

    serializer = CurrencyConverterSerializer(data=converted_data, many=True)
    if serializer.is_valid():
        serializer.save()
        logger.info(f"Serialized data: {serializer.data}")
    else:
        logger.info(f"Bad data from rates API: {serializer.errors}")


def get_rates_api() -> dict:
    return requests.get(RATES_API_URL, params={"app_id": os.environ.get("SITE_APP_ID")}).json()


def covert_info(data: dict) -> list[dict]:
    return [
        {
            "currency": key,
            "cur_to_usd": value,
        }
        for key, value in data["rates"].items()
        if key in CurrencyConverter.Currency.values and key != "USD"
    ]
