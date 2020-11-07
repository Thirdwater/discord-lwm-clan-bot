from discord.ext import commands


class ChannelController(commands.Cog):

    def __init__(self, bot, model, view):
        self.bot = bot
        self.model = model
        self.view = view

    @commands.group(name='channel', invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def channel(self, context):
        await context.send_help(context.command)

    @channel.command(name='set-verification')
    @commands.has_permissions(manage_channels=True)
    async def set_verification_channel(self, context):
        "Assigns the channel for member verification"
        pass

    @channel.command(name='get-verification')
    @commands.has_permissions(manage_channels=True)
    async def get_verification_channel(self, context):
        "Displays the channel assigned for member verification"
        channel = await self.model.persistence.get_verification_channel()
        if channel is None:
            await context.send("Verification channel has not been set.")
            await context.send_help(self.bot.get_command('channel set-verification'))
            return
        

    @channel.command(name='set-output')
    @commands.has_permissions(manage_channels=True)
    async def set_output_channel(self, context):
        "Assigns the channel to log bot outputs"
        pass

    @channel.command(name='get-output')
    @commands.has_permissions(manage_channels=True)
    async def get_output_channel(self, context):
        "Displays the channel assigned to log bot outputs"
        channel = await self.model.persistence.get_output_channel()
        if channel is None:
            await context.send("Output channel has not been set.")
            await context.send_help(self.bot.get_command('channel set-output'))
            return

    @channel.error
    @set_verification_channel.error
    @get_verification_channel.error
    @set_output_channel.error
    @get_output_channel.error
    async def command_errors(self, context, error):
        # Normal users don't need to know that these commands exist.
        pass
