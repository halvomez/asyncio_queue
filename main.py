import config
from controller import *


async def index(request):
    return web.Response(text='Welcome to API!')


def main():
    loop = asyncio.get_event_loop()
    app = web.Application()
    TaskController(app)
    workers = []

    for num in range(config.APP['workers_qty']):
        worker = WorkerController(num)
        workers.append(loop.create_task(worker.worker(loop)))

    app.router.add_get('/', index)
    web.run_app(app, port=config.APP['port'])


if __name__ == "__main__":
    main()
