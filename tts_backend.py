import asyncio

from websockets.server import serve
import logging
from bot_params import TTS_SAVE_PATH
from tts import GLaDOS

ip = '127.0.0.1' # IP of the backend.
port = 8765 # Port of the backend.
device = 'cpu' # The device used to generate TTS audio.
glados = GLaDOS(device, False) # Creates a GLaDOS TTS object.


async def tts(websocket, path):
    async for message in websocket:
        # Schedule the handle_tts coroutine to run in the background
        asyncio.create_task(handle_tts(websocket, message))


async def handle_tts(websocket, message):
    try:
        glados.tts(message, True, TTS_SAVE_PATH)
        await websocket.send('SUCCESS')
    except Exception as ex:
        logging.error("Error processing TTS request", exc_info=True)
        await websocket.send('ERROR')


async def main():
    async with serve(tts, ip, port):
        await asyncio.Future()  # run forever


asyncio.run(main())