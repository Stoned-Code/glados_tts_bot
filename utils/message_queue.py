import asyncio
import json
from collections import deque
from multiprocessing import Pool
import os

class Messages:
    @staticmethod
    def read_queue(path, callback):
        if os.path.exists(path):
            with open(path, 'rb') as f:
                jstr = f.read().decode()
            
            msg_q = Messages(callback)
            j_obj = json.loads(jstr)
            [msg_q.add(msg) for msg in j_obj]

            return msg_q
        else:
            return Messages(callback)
        
    def __init__(self, callback):
        self._msg_queue = deque()
        self.callback = callback
        self.pool = Pool(processes=1)

        print('Finished initializing message queue.')

    def to_json(self, path):
        msgs = list(self._msg_queue)
        jstr = json.dumps(msgs)

        with open(path, 'wb') as f:
            f.write(jstr.encode())

    async def loop(self):
        print('Started message loop.')
        while True:
            try:
                if len(self._msg_queue) > 0:
                    msg = self.next()
                    await self.callback(msg)
            except:
                pass
            
            await asyncio.sleep(0.5)


    def next(self):
        return self._msg_queue.pop()
    

    def add(self, msg):
        return self._msg_queue.appendleft(msg)
    

    def clear(self):
        self._msg_queue.clear()


def cb(msg):
    print(msg)

if __name__ == '__main__':
    msgs = Messages(callback=cb)