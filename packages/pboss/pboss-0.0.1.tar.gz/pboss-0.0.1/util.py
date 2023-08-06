import os, random, time

def rsleep():
    time.sleep(random.random())

class base_class(object):
    def send_message(self, to, data, pid = None, token = None):
        bus = self.bus
        if pid is None:
            try:
                pid = self.pid
                assert not pid is None
            except:
                pid = os.getpid()
                self.pid = pid
        if token is None:
            token = random.randint(1000,9999)
        msg = {
            'from': pid
            , 'to': to
            , 'data': data
            , 'token': token
            , 'ttl': 10
        }
        # print(msg)
        bus.put(msg)
        return token
    
    def get_message(self, token = None, pid = None):
        bus = self.bus
        if pid is None:
            try:
                pid = self.pid
                assert not pid is None
            except:
                pid = os.getpid()
                self.pid = pid
        while True:
            try:
                if not token is None:
                    msg = self.msg_object[token]
                    del self.msg_object[token]
                    return msg
            except KeyError:
                pass
            msg = bus.get()
            if msg['to'] == pid:
                if not token is None:
                    _token = msg['token']
                    self.msg_object[_token] = msg
                else:
                    return msg
            else:
                msg['ttl'] -= 1
                if msg['ttl'] == 0:
                    print('msg ttl == 0:',msg)
                bus.put(msg)
                rsleep()