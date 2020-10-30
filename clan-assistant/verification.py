import os
from discord.ext import commands


class VerificationCog(commands.Cog, name="Verification"):

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

    @commands.command(name='set-output-channel')
    @commands.has_permissions(manage_channels=True)
    async def set_output_channel(self, context):
        "Assigns the channel for displaying the bot's output log"
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

    @commands.command(name='get-output-channel')
    @commands.has_permissions(manage_channels=True)
    async def get_output_channel(self, context):
        "Displays which channel the bot is outputing its log"
        print(context.command)
        channel = await self.persistence.get_output_channel()
        channel_name = channel['name']
        if channel_name is None:
            print("  no output channel")
            await context.send("Output channel has not been set.")
            await context.send_help(self.bot.get_command('set-output-channel'))
            return
        print("  has output channel")
        category_string = ""
        category_name = channel['category']['name']
        if category_name is not None:
            category_string = f" in category \"{category_name}\""
        channel_string = f"Output channel:\n\"{channel_name}\"{category_string}"
        await context.send(channel_string)

    @set_verification_channel.error
    @get_verification_channel.error
    @set_output_channel.error
    @get_output_channel.error
    async def command_errors(self, context, error):
        # Normal users don't need to know that these commands exist.
        pass
