import os
from discord.ext import commands

from controllers import ChannelController


class Controller(commands.Cog):

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.bot = commands.Bot(command_prefix='!')
        self.channel_controller = ChannelController(self.bot, model, view)

        self.bot.add_cog(self)
        self.bot.add_cog(self.channel_controller)

        token = os.getenv('DISCORD_TOKEN')
        self.bot.run(token)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot controller is ready.")
