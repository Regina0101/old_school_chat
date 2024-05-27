import asyncio
import json
import aiohttp
from exchange_rate import ApiPrivatBank
from day_filter import DayCount
from datetime import datetime, timedelta
import time

async def fetch_exchange_data(days):
    if days > 10:
        print("Number of days should not be more than 10")
        return None
    dt = datetime.now()
    dates = [(dt - timedelta(days=i)).strftime('%d.%m.%Y') for i in range(days)]
    api_privat = ApiPrivatBank()
    start_time = time.time()
    data = {}
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(api_privat.fetch(date, session)) for date in dates]
        results = await asyncio.gather(*tasks)
        for date, result in zip(dates, results):
            if result is None:
                print(f"Result : {result} -- {date}")
                continue
            data[date] = result
        end_time = time.time()
        print(f"Fetched all data in {end_time - start_time:.2f} seconds")
    return data

async def get_currency_rate(days):
    data = await fetch_exchange_data(days)
    if data is not None:
        day_c = DayCount()
        currency_rate = await day_c.day_count(data)
        return currency_rate
    return {}
