from multiprocessing import Process, Queue, Event
from pboss.util import rsleep, base_class
import time, signal, random, os

def n_target(self, func, *args, **kwargs):
    self.pid = os.getpid()
    func(self, *args, **kwargs)

class base_worker(base_class):
    def __init__(self, *, bus, boss):
        self.bus = bus
        self.boss = boss
        self.msg_object = {}
    
    def new_worker(self, *args, **kwargs):
        data = {
            'type': 'r',
            'args': args,
            'kwargs': kwargs
        }
        token = self.send_message(self.boss, data)
        data = self.get_message(token = token)['data']
        # print('new_worker:',data)
        pid = data['pid']
        name = data['name']
        return package_worker(pid, name, bus = self.bus, boss = self.boss)
    
    def start_worker(self, worker):
        assert not((worker.name is None) and (worker.pid is None))
        data = {
            'type': 's',
            'worker': {
                'name': worker.name
                , 'pid': worker.pid
            }
        }
        token = self.send_message(self.boss, data)
        return self.get_message(token)['data']

    def kill_worker(self, worker):
        assert not((worker.name is None) and (worker.pid is None))
        token = None
        data = {
            'type': 'f',
            'worker': {
                'name': worker.name
                , 'pid': worker.pid
            }
        }
        self.send_message(self.boss, data)

class package_worker(base_worker):
    def __init__(self, pid, name, *args, **kwargs):
        super(package_worker, self).__init__(*args, **kwargs)
        self.pid = pid
        self.name = name
    
    def start(self):
        data = self.start_worker(self)
        self.name = data['name']
        self.pid = data['pid']

    def kill(self):
        self.kill_worker(self)

class worker(Process, base_worker):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None, boss):
        self.sub_workers = []
        self.bus = boss.bus
        self.boss = boss.pid
        pkw = package_worker(None, None, bus = self.bus, boss = self.boss)
        args = (pkw, target) + args
        Process.__init__(self, group, n_target, name, args, kwargs, daemon=daemon)