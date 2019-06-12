import asyncio
import logging
from time import sleep
from datetime import datetime
from aiohttp import web

logging.basicConfig(level='INFO')

queue = asyncio.Queue()
active_tasks = []


class TaskController(object):
    def __init__(self, app):
        self.app = app
        self.app.router.add_post('/add_task', self.add_task)
        self.app.router.add_post('/get_tasks', self.get_tasks)

    @staticmethod
    async def add_task(request: web.Request):
        data = await request.json()
        task = {
            'id': '',
            'status': 'in_queue',
            'N': data['n'],
            'D': data['d'],
            'N1': data['n1'],
            'interval': data['interval'],
            'current': [],
            'timestamp': str(datetime.now())
        }
        queue.put_nowait(task)

        return web.Response(text='task sent successfully')

    @staticmethod
    async def get_tasks(request):
        tasks = list(queue._queue)

        for task in active_tasks:
            if task is not None:
                tasks.append(task)

        if not tasks:
            return web.json_response('no tasks in the queue')

        tasks = sorted(tasks, key=lambda x: x['timestamp'])
        for index, item in enumerate(tasks, 1):
            item['id'] = index

        return web.json_response(tasks)


class WorkerController(object):
    def __init__(self, num):
        self.num = num
        self.logger = logging.getLogger(f'worker-{num + 1}')
        self.logger.setLevel('INFO')

    async def do_work(self, app):
        self.logger.info(' ready to work')
        active_tasks.append(None)
        while True:
            active_tasks[self.num] = await queue.get()
            self.logger.info(' task in progress')
            active_tasks[self.num]['status'] = 'in_progress'
            await app.loop.run_in_executor(None, self.run_progression,
                                           active_tasks[self.num])
            active_tasks[self.num] = None
            self.logger.info(' task completed and removed')
            queue.task_done()

    @staticmethod
    def run_progression(task):
        count = 1

        while count <= task['N']:
            task['current'].append(task['N1'] + task['D'] * (count - 1))

            if len(task['current']) == task['N']:
                break

            count += 1
            sleep(task['interval'])
