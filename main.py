import config
from controller import *


async def index(request):
    return web.Response(text='Welcome to API!')


async def start_background_tasks(app):
    app['workers_task'] = []

    for num in range(config.APP['workers_qty']):
        worker = WorkerController(num)
        app['workers_task'].append(app.loop.create_task(worker.do_work(app)))


async def cleanup_background_tasks(app):
    for task in app['workers_task']:
        task.cancel()
        await task


def main():
    app = web.Application()
    TaskController(app)

    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    app.router.add_get('/', index)
    web.run_app(app, port=config.APP['port'])


if __name__ == "__main__":
    main()
