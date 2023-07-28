import os

from discord import FFmpegPCMAudio, VoiceChannel
from discord.ext.commands import Bot
from discord.ext.commands.context import Context
from discord.message import Message

from bot_params import TTS_SAVE_PATH
from utils.tts_client import GLaDOS_Client


class GLaDOS_Bot:
    def __init__(self, *args, tts_channel_id = None, use_channel_id = False, **kwargs):
        self.__client = Bot(*args, **kwargs)
        self.tts_channel_id = tts_channel_id
        self.use_channel_id = use_channel_id
        self.tts_users = []
        self.glad = GLaDOS_Client()
        self.current_vc = None


    @property
    def client(self):
        return self.__client


    async def msg_queue_callback(self, msg):
        if self.current_vc == None:
            self.msg_queue.clear()
            return
        print(msg)
        await self.play_msg(msg)


    async def play_msg(self, msg):
        print('Starting TTS.')

        self.glad.get_tts_data(msg)

        src = FFmpegPCMAudio(TTS_SAVE_PATH)

        def __callback__(ob):
            src.cleanup()
            self.current_vc.cleanup()

            os.remove(TTS_SAVE_PATH)


        print('Playing audio.')
        self.current_vc.play(src, after=__callback__)


    async def __connect__(self, ctx: Context or Message):
        channels = ctx.guild.voice_channels
        user_id = ctx.author.id

        channels = [channel for channel in channels if self.has_member(channel, user_id)]
        if len(channels) < 1:
            return
        
        if self.current_vc == None:
            self.current_vc = await channels[0].connect()
    

    async def __disconnect__(self):
        await self.current_vc.disconnect()
        self.current_vc = None


    def has_member(self, channel: VoiceChannel, id):
        users = channel.members
        users = [user.id for user in users]

        return id in users
    

    def add_tts(self, msg, *content):
        user_id = msg.author.id
        user_name = msg.author.name

        channels = msg.guild.voice_channels
        channels = [channel for channel in channels if self.has_member(channel, user_id)]

        if len(channels) != 1:
            return
        
        if user_name not in self.tts_users:
            self.tts_users.append(user_name)
        

        template = '{} says: {}'
        template = template.format(msg.author.display_name, msg.content if len(content) < 1 else ' '.join(list(content)))

        self.msg_queue.add(template)


    def add_tts(self, msg):
        self.msg_queue.add(msg)