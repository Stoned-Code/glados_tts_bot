import asyncio
from websockets.server import serve
import json
from tts import GLaDOS
from bot_params import TTS_SAVE_PATH


ip = '127.0.01'
port = 8765
device = 'cpu'
glados = GLaDOS(device, False)


async def tts(websocket):
    async for message in websocket:

        glados.tts(message, True, TTS_SAVE_PATH)

        await websocket.send('SUCCESS')


async def main():
    async with serve(tts, ip, port):
        await asyncio.Future()  # run forever


asyncio.run(main())