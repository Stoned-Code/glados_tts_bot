import discord, asyncio
from discord.message import Message
from discord import VoiceState
from bot_params import PREFIX

class BotEvents:
        def __init__(self, g_bot, use_channel_id, tts_channel, auto_connect):
            self.g_bot = g_bot

            @g_bot.client.event
            async def on_ready():
                asyncio.get_event_loop().create_task(g_bot.msg_queue.loop())
                
                print(f'Logged in as {g_bot.client.user} (ID: {g_bot.client.user.id})')
                await self.g_bot.client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, 
                                                                    name = 'Help: {}help | Prefix: {}'.format(PREFIX, PREFIX)))

            @g_bot.client.event
            async def on_message(msg: Message):
                if msg.content.startswith(PREFIX) or msg.author.id == g_bot.client.user.id:
                    await self.g_bot.client.process_commands(msg)
                    return
                
                # if g_bot.current_vc != None:
                #     await msg.send('I apologize for the inconvenience, but it seems I am currently engaged in another voice channel. Please wait until I am available, or try again later. Thank you for your understanding.')
                
                if use_channel_id:
                    if msg.channel.id != tts_channel:
                        return
                else:
                    if not msg.channel.name.startswith('tts-'):
                        return
                    
                if auto_connect:
                    await self.g_bot.__connect__(msg)

                    self.g_bot.add_tts(msg)


            @g_bot.client.event
            async def on_voice_state_update(member: discord.member.Member, before: VoiceState, after: VoiceState):
                if not member.name in g_bot.tts_users:
                    return
                
                in_tts = member.name in g_bot.tts_users
                channel_flag = before.channel.id == g_bot.current_vc.channel.id
                none_after = after.channel == None
                flag = in_tts and channel_flag and none_after


                if flag:
                    self.g_bot.tts_users.remove(member.name)

                    if len(self.g_bot.tts_users) < 1:
                        await self.g_bot.__disconnect__()
