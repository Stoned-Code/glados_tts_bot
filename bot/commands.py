from discord.ext.commands.context import Context

class BotCommands:
    def __init__(self, g_bot, sc_coms):
        self.g_bot = g_bot
        @sc_coms.add_command(description='Disconnects the bot from the voice channel it\'s in.')
        @g_bot.client.command()
        async def disconnect(ctx: Context):
            await self.g_bot.current_vc.disconnect()
            #print(type(g_bot.current_vc))
            self.g_bot.current_vc = None


        @sc_coms.add_command(description='Connects the bot to the channel the user is in. And if a message is given, it will be the first message played.', 
                example='connect {optional: msg}', argumentDescriptions=['msg: Optional - A message that will be played a little after joining.'])
        @g_bot.client.command()
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