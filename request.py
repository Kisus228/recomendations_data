import prometheus_client
from aiohttp import web
from prometheus_client import Gauge
import asyncio
import aiohttp
from json import loads
from calculations import get_metric, get_metric_production

GAUGE_METRIC = Gauge('metrics_monitoring', 'data tracking')


async def create_metrics_response(request):
    resp = web.Response(body=prometheus_client.generate_latest())
    resp.content_type = prometheus_client.CONTENT_TYPE_LATEST
    return resp


async def keep_update_gauge():
    async with aiohttp.ClientSession() as session:
        while True:
            task = asyncio.create_task(create_url_data(session))
            await asyncio.gather(task)


async def create_url_data(session):
    async with session.post(url, json=dates, headers=headers) as response:
        data = await response.json()
        data = loads(data)
        # metric = get_metric_production(data)
        metric = get_metric(data)
        GAUGE_METRIC.set(metric)
        print(metric)
        await asyncio.sleep(time_sleep)


def main():
    http_app = web.Application()
    http_app.router.add_get("/metrics", create_metrics_response)
    ioloop = asyncio.get_event_loop()
    tasks = [ioloop.create_task(keep_update_gauge()), ioloop.create_task(web.run_app(http_app, port=8000))]
    ioloop.run_until_complete(asyncio.wait(tasks))

    # asyncio.run(keep_update_gauge())
    # web.run_app(httpApp, port=8000)


dates = {'start': '01.01.2018', 'finish': '12.31.2018'}
time_sleep = 3
headers = {"Content-Type": "application/json", "X-Auth-Token": "4CE7B412-49B7-3DCF-B56D-3441B6A3698A"}
url = 'http://localhost:8080/execmodel'

if __name__ == '__main__':
    main()


