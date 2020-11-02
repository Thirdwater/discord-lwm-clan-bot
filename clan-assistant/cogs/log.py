from discord.ext import commands


class Log(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.persistence = self.bot.get_cog("Persistence")

    @commands.command(name='set-output-channel')
    @commands.has_permissions(manage_channels=True)
    async def set_output_channel(self, context):
        "Assigns the channel for displaying the bot's output log"
        channel = context.channel

    @commands.command(name='get-output-channel')
    @commands.has_permissions(manage_channels=True)
    async def get_output_channel(self, context):
        "Displays which channel the bot is outputing its log"
        print(context.command)
        channel = await self.persistence.get_output_channel()
        channel_name = channel['name']
        if channel_nae is None:
            print("  no output channel")
            await context.send("Output channel has not ben set.")
            await context.send_help(self.bot.get_command('set-output-channel'))
            return
        print("  has output channel")
        category_string = ""
        category_name = channel['channel']['name']
        if category_name is not None:
            category_string = f" in category \"{category_name}\""
        channel_string = f"Output channel:\n\"{channel_name}\"{category_string}"
        await context.send(channel_string)

    @set_output_channel.error
    @get_output_channel.error
    async def command_errors(self, context, error):
        # Normal users don't need to know that these commands exist.
        pass
