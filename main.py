import asyncio
import os
from random import choice

import discord
from discord import VoiceState
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message

from bot_params import CHARACTERS, PREFIX, Q_PATH, TTS_FILE_FOLDER
from utils.message_queue import Messages
from utils.sc_bots import GLaDOS_Bot
# from sc_libs.discord.command import SCCommand
# from sc_libs.discord.help import SCHelp
from utils.tts_client import GLaDOS_Client


token = 'token.txt'


def read_token(token):
    if not os.path.exists(token):
        raise Exception('\'{}\' not defined.'.format(token))

    with open(token, 'r') as f:
        token = f.read()

    return token


def init_folder(path):
    if os.path.exists(path):
        return
    else:
        os.mkdir(path)


token = read_token(token)
tts_channel = 1132143033798901850
use_channel_id = True
intents = discord.Intents.all()


g_bot = GLaDOS_Bot(command_prefix=PREFIX, tts_channel_id=tts_channel, use_channel_id=use_channel_id, intents = intents)
g_client = GLaDOS_Client()

#SCCommand.set_prefix(PREFIX)

# sc_help = SCHelp(g_bot)
# sc_help.set_bot_description('A TTS discord bot that uses the GLaDOS model at the github repository: https://github.com/nerdaxic/glados-tts.')
# sc_help.set_thumbnail('https://images-na.ssl-images-amazon.com/images/I/71uXB4Kj4BL.png')

async def msg_queue_callback(msg):
    if g_bot.current_vc == None:
        g_bot.msg_queue.clear()
        return

    await g_bot.play_msg(msg)


if os.path.exists(Q_PATH):
    g_bot.msg_queue = Messages.read_queue(Q_PATH, msg_queue_callback)
    
else:
    g_bot.msg_queue = Messages(msg_queue_callback)


def random_characters(amt = 5):
    return ''.join([choice(CHARACTERS.split()) for i in range(amt)])


@g_bot.client.event
async def on_ready():
    asyncio.get_event_loop().create_task(g_bot.msg_queue.loop())
    
    print(f'Logged in as {g_bot.client.user} (ID: {g_bot.client.user.id})')
    await g_bot.client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, 
                                                        name = 'Help: {}help | Prefix: {}'.format(PREFIX, PREFIX)))

@g_bot.client.event
async def on_message(msg: Message):
    if msg.content.startswith(PREFIX) or msg.author.id == g_bot.client.user.id:
        return
    
    if g_bot.current_vc != None:
        await msg.send('I apologize for the inconvenience, but it seems I am currently engaged in another voice channel. Please wait until I am available, or try again later. Thank you for your understanding.')
    
    if use_channel_id:
        if msg.channel.id != tts_channel:
            return
    else:
        if not msg.channel.name.startswith('tts-'):
            return
    
    await g_bot.__connect__(msg)

    user_id = msg.author.id
    user_name = msg.author.name

    channels = msg.guild.voice_channels
    channels = [channel for channel in channels if g_bot.has_member(channel, user_id)]

    if len(channels) != 1:
        return
    
    if user_name not in g_bot.tts_users:
        g_bot.tts_users.append(user_name)

    template = '{} says: {}'
    template = template.format(msg.author.display_name, msg.content)

    g_bot.msg_queue.add(template)


@g_bot.client.event
async def on_voice_state_update(member: discord.member.Member, before: VoiceState, after: VoiceState):
    if not member.name in g_bot.tts_users:
        return
    
    in_tts = member.name in g_bot.tts_users
    channel_flag = before.channel.id == g_bot.current_vc.channel.id
    none_after = after.channel == None
    flag = in_tts and channel_flag and none_after

    # print(in_tts)
    # print(channel_flag)
    # print(none_after)
    # print(flag)

    if flag:
        g_bot.tts_users.remove(member.name)
        print(g_bot.tts_users)
        if len(g_bot.tts_users) < 1:
            await g_bot.__disconnect__()
            print('Disconnected.')


@g_bot.client.command(name='tts')
async def text_2_speach(ctx: Context, *msg):
    print('Hello there.')
    await ctx.send('One moment...')
    user = ctx.author.display_name.lower().replace(' ', '')
    rand = random_characters()

    file_name = '{}_{}.wav'.format(user, rand)

    file_name = os.path.join('./files', file_name)

    await ctx.reply('Your TTS file.', file = discord.File(file_name))

    os.remove(file_name)


@g_bot.client.command()
async def disconnect(ctx: Context):
    await g_bot.current_vc.disconnect()
    print(type(g_bot.current_vc))
    g_bot.current_vc = None


@g_bot.client.command()
async def connect(ctx: Context):
    channels = ctx.guild.voice_channels
    user_id = ctx.author.id

    channels = [channel for channel in channels if g_bot.has_member(channel, user_id)]

    if g_bot.current_vc != None:
        pass
    else:
        g_bot.current_vc = await channels[0].connect()


init_folder(TTS_FILE_FOLDER)
g_bot.client.run(token)
