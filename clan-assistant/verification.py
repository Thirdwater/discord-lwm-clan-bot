import os
from discord.ext import commands


class VerificationCog(commands.Cog, name="Verification"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        channel = message.channel
        print(f"Received message from {message.author} in {channel}")

    @commands.command(name='set-verification-channel')
    @commands.has_permissions(manage_channels=True)
    async def set_verification_channel(self, context):
        "Assigns the bot to check for profile links in the specified channel."
        channel = context.message.channel

    @commands.command(name='display-verification-channel')
    @commands.has_permissions(manage_channels=True)
    async def display_verification_channel(self, context):
        "Displays which channel the bot is checking for profile links."
        pass

    @set_verification_channel.error
    @display_verification_channel.error
    async def verification_channel_error(self, context, error):
        # Normal users don't need to know that these commands exist.
        pass
