import os
from random import choice
import discord
from discord.ext.commands.context import Context
from bot_params import PREFIX, Q_PATH, TTS_FILE_FOLDER
from utils.message_queue import Messages
from utils.sc_bots import GLaDOS_Bot
from sc_libs.discord.command import SCCommands
from sc_libs.discord.help import SCHelp
from utils.tts_client import GLaDOS_Client
from bot import events
from bot import commands as sc_commands


token = 'token.txt' # Sets a token path to a variable.


def read_token(token):
    if not os.path.exists(token): # Checks if the token path exists.
        raise Exception('\'{}\' not defined.'.format(token)) # Raises an exception if the token doesn't exist.

    with open(token, 'r') as f:
        token = f.read() # Reads the token from the file path.

    return token # Returns the token.


def init_folder(path):
    if os.path.exists(path):
        return
    
    else:
        os.mkdir(path)


token = read_token(token)
#tts_channel = 1134547317593219092
tts_channel = 1132143033798901850
use_channel_id = False
auto_connect = True
intents = discord.Intents.all()


g_bot = GLaDOS_Bot(command_prefix=PREFIX, tts_channel_id=tts_channel, use_channel_id=use_channel_id, intents = intents)
g_client = GLaDOS_Client()

sc_coms = SCCommands(PREFIX)


sc_help = SCHelp(g_bot.client, sc_coms)
sc_help.set_bot_description('A TTS discord bot that uses the GLaDOS model at the github repository: https://github.com/nerdaxic/glados-tts.')
sc_help.set_thumbnail('https://images-na.ssl-images-amazon.com/images/I/71uXB4Kj4BL.png')

bot_events = events.BotEvents(g_bot, use_channel_id, tts_channel, auto_connect)
bot_commands = sc_commands.BotCommands(g_bot, sc_coms)

async def msg_queue_callback(msg):
    if g_bot.current_vc == None:
        g_bot.msg_queue.clear()
        return

    await g_bot.play_msg(msg)


if os.path.exists(Q_PATH):
    g_bot.msg_queue = Messages.read_queue(Q_PATH, msg_queue_callback)

else:
    g_bot.msg_queue = Messages(msg_queue_callback)

init_folder(TTS_FILE_FOLDER)
g_bot.client.run(token)
