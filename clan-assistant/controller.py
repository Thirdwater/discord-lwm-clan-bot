import os
from discord.ext import commands


class Controller(commands.Cog):

    def __init__(self, model, view):
        self.model = model
        self.view = view

        token = os.getenv('DISCORD_TOKEN')
        self.bot = commands.Bot(command_prefix='!')
        self.bot.add_cog(self)
        self.bot.run(token)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot controller is ready.")

    @commands.group(name='get', invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def get(self, context):
        await context.send_help(context.command)

    @commands.group(name='set', invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def set(self, context):
        await context.send_help(context.command)

    @get.error
    @set.error
    async def command_errors(self, context, error):
        # Normal users don't need to know that these commands exist.
        pass
