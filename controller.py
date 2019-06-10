import asyncio
import logging
from datetime import datetime
from aiohttp import web

logging.basicConfig(level='INFO')


class ProgressionController(object):
    def __init__(self, app):
        self.app = app
        self.queue = asyncio.Queue()
        self.active_task = None
        self.app.router.add_post('/add_task', self.add_task)
        self.app.router.add_post('/get_tasks', self.get_tasks)

        self.logger = logging.getLogger('queue_worker')
        self.logger.setLevel('INFO')

    async def add_task(self, request: web.Request):
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

        self.queue.put_nowait(task)

        return web.Response(text='task sent successfully')

    async def get_tasks(self, request):
        tasks = list(self.queue._queue)
        if self.active_task:
            tasks.append(self.active_task)

        if not tasks:
            return web.json_response('no tasks in the queue')

        tasks = sorted(tasks, key=lambda x: x['timestamp'])
        for index, item in enumerate(tasks, 1):
            item['id'] = index

        return web.json_response(tasks)

    async def worker(self):
        self.logger.info('queue_worker is starting')
        while True:
            self.active_task = await self.queue.get()
            self.active_task['status'] = 'in_progress'
            await self.run_progression()
            self.active_task = None
            self.logger.info('task completed and removed')
            self.queue.task_done()

    async def run_progression(self):
        count = 1

        while count <= self.active_task['N']:
            self.active_task['current'].append(self.active_task['N1'] +
                                               self.active_task['D'] *
                                               (count - 1))
            if len(self.active_task['current']) == self.active_task['N']:
                break

            count += 1
            await asyncio.sleep(self.active_task['interval'])
