from aiohttp import web
from settings import log, config
import pandas as pd
import os
import json

file_name = 'recom_events.csv'

with open(os.path.abspath(os.path.join(os.path.abspath(os.curdir),
                                       "static/", str(file_name))),
          'rb') as f:
    df = pd.read_csv(f)
    df['DATE'] = pd.to_datetime(df['DATE'])


def modpred(start, finish):
    try:
        result = df[df['DATE'].between(pd.to_datetime(start), pd.to_datetime(finish))]
        return result.to_json(orient="records")
    except Exception as e:
        log.debug(f'error: {e}')
        return json.dumps({"ERROR": str(repr(e)), "Data": None})


class Execution(web.View):
    async def post(self):
        log.info(
            "rest api request ... /execmodel from " + str(self.request.remote))
        if (self.request.headers.get("X-Auth-Token") !=
                config.AUTHENTICATION_TOKEN_EXECMODEL):
            log.info("error authentication token ... " + "from " +
                     str(self.request.remote) + " [" +
                     str(self.request.headers.get('X-Auth-Token')) + ']')
            return web.Response(
                status=401,
                text=str('{"error":"authentication token"}')
            )
        log.info("authentication token ... " +
                 "from " + str(self.request.remote) + " [Ok]")
        if self.request.headers.get("Content-Type") != "application/json":
            log.info("error request ... " +
                     "is not application/json")
            return web.Response(
                status=401,
                text=str('{"error":"request is not application/json"}')
            )
        log.info("exec model ... start")
        try:
            data = await self.request.json()
            log.info(f"input json: {data}")
            if "start" in list(data.keys()):
                start = str(data["start"])
            else:
                start = "01.01.2018"
            if "finish" in list(data.keys()):
                finish = str(data["finish"])
            else:
                finish = "01.01.2023"
        except Exception as e:
            log.debug(f'error: {e}')
            data = "Cannot parse json"
            log.debug(f'input json: {data}')
            return web.Response(
                status=400,
                text=str('{"error":"request is not application/json"}')
            )
        try:
            log.info("exec model ... start")
            model_exec_result = modpred(start, finish)
            log.info("exec model ... end")
        except Exception as e:
            log.debug(f"Error: {e}")
            return web.Response(status=400, text=str(e))
        if "ERROR" in model_exec_result:
            status = 401
        else:
            status = 200
        return web.json_response(status=status, data=model_exec_result)


""" описание метода быстрой проверки работоспособности микросервиса """


class Ping(web.View):
    async def get(self):
        log.info(
            "rest api request ... /pingmodel from " + str(self.request.remote))
        if (self.request.headers.get("X-Auth-Token") !=
                config.AUTHENTICATION_TOKEN_PINGMODEL):
            log.info("error authentication token ... " + "from " +
                     str(self.request.remote) +
                     " [" + str(self.request.headers.get("X-Auth-Token")) +
                     "]")
            return web.Response(
                status=401,
                text=str('{"error":"authentication token"}')
            )
        log.info("authentication token ... " +
                 "from " + str(self.request.remote) + " [Ok]")
        log.debug(str('{"status":"started"}'))
        text = '{"status":"started"}'
        return web.Response(text=text)


class Healthcheck(web.View):
    async def get(self):
        log.debug("Healthcheck")
        text = '{"status":"ok"}'
        content_type = "application/json"
        return web.Response(
            text=text,
            content_type=content_type
        )
