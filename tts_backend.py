import asyncio

from websockets.server import serve
import logging
from bot_params import TTS_SAVE_PATH
from tts import GLaDOS

ip = '127.0.0.1'
port = 8765
device = 'cpu'
glados = GLaDOS(device, False)


# async def tts(websocket):
#     async for message in websocket:
#         try:
#             glados.tts(message, True, TTS_SAVE_PATH)

#             await websocket.send('SUCCESS')
#         except Exception as ex:
#             print(ex.with_traceback(None))
#             await websocket.send('ERROR')



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