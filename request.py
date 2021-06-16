import prometheus_client
from aiohttp import web
from prometheus_client import Gauge
import asyncio

GAUGE_METRIC = Gauge('metrics_monitoring', 'data tracking')


async def create_metrics_response(request):
    resp = web.Response(body=prometheus_client.generate_latest())
    resp.content_type = prometheus_client.CONTENT_TYPE_LATEST
    return resp


def keep_update_gauge():
    pass
    #TODO добавить асинхронное обновление метрики через while(true), и лучше с интервалом через asyncio.sleep(*время*). GAUGE_METRICS.set(*метрика*)
    #TODO почистить проект от лишних методов вычислений. Я про файлы calculations_1 и calculations. Просто почистить проект


def main():
    httpApp = web.Application()
    httpApp.router.add_get("/metrics", create_metrics_response)
    keep_update_gauge()
    web.run_app(httpApp)


if __name__ == '__main__':
    main()
