# -*- coding: utf-8 -*-
import click
from routers import routes
from aiohttp import web
from settings import config, log


@click.group()
def cli():
    pass


@cli.command()
def run():
    app = web.Application(client_max_size=50000000)

    # route part
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])

    log.info("start server")
    web.run_app(app, host=config.HOST, port=config.PORT)
    log.info("Stop server end")


if __name__ == "__main__":
    run()
    cli()
