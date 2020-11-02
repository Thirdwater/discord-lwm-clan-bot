import os
from discord.ext import commands

from lordswm import LWMInterface


class Clan(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.persistence = self.bot.get_cog("Persistence")
        self.lwm = LWMInterface()

    @commands.group(name='query', aliases=['check'], invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def query(self, context):
        "Queries various statistics from the clan"
        await context.send_help(context.command)

    @query.command(name='verified')
    @commands.has_permissions(manage_channels=True)
    async def query_verified_members(self, context):
        "Lists all verified members from the clan"
        pass

    @query.command(name='unverified')
    @commands.has_permissions(manage_channels=True)
    async def query_unverified_members(self, context):
        "Lists all unverified members from the clan"
        pass

    @query.command(name='participants')
    @commands.has_permissions(manage_channels=True)
    async def query_event_participants(self, context):
        "Lists all event participants in the clan"
        pass

    @query.command(name='non-participants')
    @commands.has_permissions(manage_channels=True)
    async def query_non_event_participants(self, context):
        "Lists all event non-participants in the clan"
        pass

    @query.error
    @query_verified_members.error
    @query_unverified_members.error
    @query_event_participants.error
    @query_non_event_participants.error
    async def query_error(self, context, error):
        # Normal users don't need to know that these commands exist.
        pass
