import asyncio
import config
from aiohttp import web
from controller import ProgressionController


async def index(request):
    return web.Response(text='Welcome to API!')


def main():
    app = web.Application()
    controller = ProgressionController(app)
    loop = asyncio.get_event_loop()
    loop.create_task(controller.worker())
    app.router.add_get('/', index)
    web.run_app(app, port=config.APP['port'])


if __name__ == "__main__":
    main()
