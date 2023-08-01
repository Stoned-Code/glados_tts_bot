import os
from random import choice

import discord
from discord.ext.commands.context import Context

from bot import commands as sc_commands
from bot import events
from bot_params import PREFIX, Q_PATH, TTS_FILE_FOLDER
from sc_libs.discord.command import SCCommands
from sc_libs.discord.help import SCHelp
from utils.bot_files import *
from utils.message_queue import Messages
from bot.glados import GLaDOS_Bot
from utils.tts_client import GLaDOS_Client


async def msg_queue_callback(msg):
    if g_bot.current_vc == None:
        g_bot.msg_queue.clear()
        return

    await g_bot.play_msg(msg)


if __name__ == '__main__':
    token = 'token.txt' # Sets a token path to a variable.
    token = read_token(token) # Reads thetoken from the file.

    tts_channel = 1134547317593219092 # The channel ID that the bot will respond in.
    use_channel_id = True # Use if you want to use any channel that has "tts-" in the beginning.
    auto_connect = True # If enabled, will auto connect the bot to the voice channel the user is in.

    intents = discord.Intents.all() # Specifies all intents.
    g_bot = GLaDOS_Bot(command_prefix=PREFIX, tts_channel_id=tts_channel, use_channel_id=use_channel_id, intents = intents) # Creates a GLaDOS discord bot object.
    g_client = GLaDOS_Client() # Creates the client used for sending TTS messages to the TTS socket.
    sc_coms = SCCommands(PREFIX) # An object that helps to keep track of bot commands.
    # uses SCCommands object to create a new help command.
    sc_help = SCHelp(g_bot.client, sc_coms, 'A TTS discord bot that uses the GLaDOS model at the github repository: https://github.com/nerdaxic/glados-tts.', 'https://images-na.ssl-images-amazon.com/images/I/71uXB4Kj4BL.png')

    g_bot.msg_queue = Messages.read_queue(Q_PATH, msg_queue_callback) # If there is a message queue, it will read it.

    bot_events = events.BotEvents(g_bot, use_channel_id, tts_channel, auto_connect) # An object with all used bot events.
    bot_commands = sc_commands.BotCommands(g_bot, sc_coms) # An object with all used bot commands.

    init_folder(TTS_FILE_FOLDER) # Makes sure that the file folder is made.
    g_bot.client.run(token) # Runs the bot client using the token read from the "read_token" command.
