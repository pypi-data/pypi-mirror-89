from .worker import base_worker, worker
from .util import base_class
from multiprocessing import Process, Queue, Event
import os

class package_boss(base_worker):
    def __init__(self, func):
        q = Queue()
        self._boss = Process(target = func, args = (q, ))
        self._boss.start()
        self.pid = os.getpid()
        super(package_boss, self).__init__(bus = q, boss = self._boss.pid)
    
    def end(self):
        data = {
            'type':'e',
        }
        self.send_message(self.boss, data)
    
    def join(self):
        self._boss.join()

class boss(base_class):
    def __init__(self, q): 
        self.workers = {}
        self.bus = q
        self.pid = os.getpid()
        self.handler = {}
        self.handler['f'] = self.kill_worker
        self.handler['r'] = self.new_worker
        self.handler['s'] = self.start
        self.handler['e'] = self.end
        self.isend = False

    def _kill_worker(self, worker):
        token = None
        if worker['pid'] is None:
            token = worker['name']
        else:
            token = worker['pid']
        assert not token is None
        worker = self.workers[token]
        if len(worker.sub_workers) > 0:
            for i in worker.sub_workers:
                self._kill_worker(i)
        del self.workers[token]
        worker.terminate()
    
    def kill_worker(self, data):
        self._kill_worker(data['worker'])
        return None

    def new_worker(self, data):
        w = worker(*data['args'], **data['kwargs'], boss = self)
        self.workers[w.name] = w
        data = {
            'name': w.name
            , 'pid' : w.pid
        }
        return data
    
    def start(self, data):
        w = self.workers[data['worker']['name']]
        w.start()
        del self.workers[data['worker']['name']]
        self.workers[w.pid] = w
        data = {
            'name': w.name
            , 'pid' : w.pid
        }
        return data

    def data_handler(self, msg):
        data = msg['data']
        res = self.handler[data['type']](data)
        if not res is None:
            data = res
            # print(data)
            self.send_message(msg['from'], data, token = msg['token'])
    
    def end(self, data):
        for i in workers.values():
            i.kill()
        self.isend = True

    def listen(self):
        msg = None
        while not self.isend:
            msg = self.get_message()
            # print('boss get msg:', msg)
            self.data_handler(msg)