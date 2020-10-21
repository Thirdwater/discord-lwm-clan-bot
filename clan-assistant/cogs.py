import os
import json
from discord.ext import commands
from discord import utils


class ClanAssistantCog(commands.Cog, name="Clan Assistant"):

    def __init__(self, bot):
        self.bot = bot
        self.load_config()

    def load_config(self):
        config_filename = os.getenv('CONFIG_FILENAME')
        if not os.path.isfile(config_filename):
            self.servers_config = {}
            return
        with open(config_filename) as config_file:
            self.servers_config = json.load(config_file)

    async def save_config(self):
        config_filename = os.getenv('CONFIG_FILENAME')
        with open(config_filename, 'w') as config_file:
            json.dump(self.servers_config, config_file, sort_keys=True, indent=4)
        print("Server configurations have been updated.")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} has connected to Discord.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

    @commands.command(name='set-verification-channel')
    @commands.has_permissions(manage_channels=True)
    async def set_verification_channel(self, context):
        "Assigns the bot to check for profile links in the specified channel."
        print(context.command)
        channel = context.message.channel
        guild = channel.guild
        category = None
        if channel.category_id:
            category = utils.get(guild.categories, id=channel.category_id)
        category_string = ""
        if category:
            category_string = f"{category.name}: "
        print(f"Channel: {channel.id}\t{category_string}{channel.name}")

        accepted_clans = []
        if str(guild.id) in self.servers_config:
            data = self.servers_config.pop(str(guild.id))
            accepted_clans = data['clans']
        self.servers_config[str(guild.id)] = {
                'server_name': guild.name,
                'category_id': category.id if category else None,
                'category_name': category.name if category else None,
                'channel_id': channel.id,
                'channel_name': channel.name,
                'clans': accepted_clans}
        await self.save_config()

    @set_verification_channel.error
    async def set_verification_channel_error(self, context, error):
        # Normal users don't need to know that these commands exist.
        pass

    @commands.group(name='clan', invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def clan(self, context):
        "Manages clan-to-discord registrations"
        await context.send_help(context.command)

    @clan.command(name='list', aliases=['ls'])
    @commands.has_permissions(manage_channels=True)
    async def list_clans(self, context):
        "Shows all clans registered to this discord server"
        print(context.command)

    @clan.command(name='register', aliases=['add', 'new'])
    @commands.has_permissions(manage_channels=True)
    async def register_clan(self, context):
        "Registers the specified clan to this discord server"
        print(context.command)

    @clan.command(name='remove', aliases=['delete', 'del', 'rm'])
    @commands.has_permissions(manage_channels=True)
    async def remove_clan(self, context):
        "Removes the specified clan from this discord server"
        print(context.command)

    @clan.error
    @list_clans.error
    @register_clan.error
    @remove_clan.error
    async def clan_error(self, context, error):
        # Normal users don't need to know that these commands exist.
        pass
