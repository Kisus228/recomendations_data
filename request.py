import aiohttp
import asyncio
from calculations import get_groups_bd, get_dict_month_metric


async def run_session(url, dates, headers):
    async with aiohttp.ClientSession() as session:
        while True:
            task = asyncio.create_task(create_url_data(url, session, dates, headers))
            await asyncio.gather(task)


async def create_url_data(url, session, dates, headers):
    async with session.post(url, json=dates, headers=headers) as responce:
        data = await responce.json()
        dict_month_metric = get_dict_month_metric(get_groups_bd(data))
        print_metrics(dict_month_metric)
        await asyncio.sleep(10)


def print_metrics(dict_month_metric):
    for date, metric in dict_month_metric.items():
        print(date, metric)


headers = {"Content-Type": "application/json", "X-Auth-Token": "4CE7B412-49B7-3DCF-B56D-3441B6A3698A"}
url = 'http://localhost:8080/execmodel'
dates = {'start': '01.01.2018', 'finish': '08.01.2018'}
asyncio.run(run_session(url, dates, headers))

#          'finish': input('Введите дату конца выбоки в формате ММ.ДД.ГГГГ\n')}
# dates = {'start': input('Введите дату начала выбоки в формате ММ.ДД.ГГГГ\n'),
