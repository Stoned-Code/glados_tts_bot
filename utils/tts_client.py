import asyncio

from websockets.sync.client import connect


class GLaDOS_Client:
    def __init__(self, ip = '127.0.0.1', port = 8765):
        self.ip = ip
        self.port = port

    def get_tts_data(self, txt):
        with connect('ws://{}:{}'.format(self.ip, self.port)) as ws:
            ws.send(txt)
            msg = ws.recv()
            #print(msg)
            return msg
        

if __name__ == '__main__':
    g = GLaDOS_Client()

    data = g.get_tts_data("hello there.")


    print(data)
    print(type(data))