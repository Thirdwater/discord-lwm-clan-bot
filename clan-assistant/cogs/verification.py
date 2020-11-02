from discord.ext import commands


class Verification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.persistence = self.bot.get_cog("Persistence")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        channel = message.channel
        print(f"Received message from {message.author} in {channel}")

    @commands.command(name='set-verification-channel')
    @commands.has_permissions(manage_channels=True)
    async def set_verification_channel(self, context):
        "Assigns the channel for the bot to check for profile links"
        channel = context.channel

    @commands.command(name='get-verification-channel')
    @commands.has_permissions(manage_channels=True)
    async def get_verification_channel(self, context):
        "Displays which channel the bot is checking for profile links."
        print(context.command)
        channel = await self.persistence.get_verification_channel()
        channel_name = channel['name']
        if channel_name is None:
            print("  no verification channel")
            await context.send("Verification channel has not been set.")
            await context.send_help(self.bot.get_command('set-verification-channel'))
            return
        print("  has verification channel")
        category_string = ""
        category_name = channel['category']['name']
        if category_name is not None:
            category_string = f" in category \"{category_name}\""
        channel_string = f"Verification channel:\n\"{channel_name}\"{category_string}"
        await context.send(channel_string)

    @set_verification_channel.error
    @get_verification_channel.error
    async def command_errors(self, context, error):
        # Normal users don't need to know that these commands exist.
        pass
