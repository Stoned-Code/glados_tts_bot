# GLaDOS TTS Bot
A Text-to-Speach bot that uses the [GLaDOS Tacotron2](https://github.com/nerdaxic/glados-tts) model to generate speach from text in a specified channel. 

## How it works. 
Uses two different processes to run properly.
1. tts_socket.py - The `tts_socket.py` script runs the GLaDOS TTS model, and saves the audio to a path.
2. main.py - The `main.py`` script runs the bot and sends messages to turn into speech to the tts_socket.py process using websockets. Then, it loads the file it saves and plays it in the voice channel.

When someone uses the TTS channel, the bot will automatically join, and add them to a list of users currently using the TTS bot. Every time someone that uses the TTS bot leaves, it removes them from the user list. When there is no longer anyone in the list, the bot automatically leaves.
