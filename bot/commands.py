from discord.ext.commands.context import Context


class BotCommands:
    def __init__(self, g_bot, sc_coms):
        self.g_bot = g_bot
        self.sc_coms = sc_coms

        self.load_commands()

        
    def load_commands(self):
        @self.sc_coms.add_command(description='Disconnects the bot from the voice channel it\'s in.')
        @self.g_bot.client.command()
        async def disconnect(ctx: Context):
            await self.g_bot.current_vc.disconnect()
            #print(type(g_bot.current_vc))
            self.g_bot.current_vc = None
            self.g_bot.msg_queue.clear()


        @self.sc_coms.add_command(description='Connects the bot to the channel the user is in. And if a message is given, it will be the first message played.', 
                example='connect {optional: msg}', argumentDescriptions=['msg: Optional - A message that will be played a little after joining.'])
        @self.g_bot.client.command()
        async def connect(ctx: Context, *msg):
            channels = ctx.guild.voice_channels
            user_id = ctx.author.id

            channels = [channel for channel in channels if self.g_bot.has_member(channel, user_id)]

            if self.g_bot.current_vc != None:
                pass
            else:
                self.g_bot.current_vc = await channels[0].connect()
            
            if len(msg) > 0:
                self.g_bot.add_tts(ctx, *msg)


        @self.sc_coms.add_command(description='An echo command for the bot.', example='say {msg}', argumentDescriptions='msg: Optional - A message for the bot to say')
        @self.g_bot.client.command()
        async def say(ctx, *msg):
            if self.g_bot.current_vc == None:
                channels = ctx.guild.voice_channels
                user_id = ctx.author.id
                channels = [channel for channel in channels if self.g_bot.has_member(channel, user_id)]

            if len(msg) < 0:
                await ctx.send('You must specify a message')
            
            msg = ' '.join(msg)

            self.g_bot.add_tts(msg)
            