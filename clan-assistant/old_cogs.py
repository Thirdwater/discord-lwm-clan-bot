import os
import json
from discord.ext import commands
from discord import utils
from discord.errors import Forbidden

from lordswm import LWMInterface


class ClanAssistantCog(commands.Cog, name="Clan Assistant"):

    def __init__(self, bot):
        self.bot = bot
        self.load_config()
        self.lwm_interface = LWMInterface()

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

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} has connected to Discord.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        channel = message.channel
        guild = channel.guild
        if str(guild.id) not in self.servers_config:
            return
        verification_channel_id = self.servers_config[str(guild.id)]['channel']['id']
        if channel.id != verification_channel_id:
            return
        if len(message.content) == 0 or message.content[0] == "!":
            return
        non_member_role = utils.get(guild.roles, name='Unverified')
        member_role = utils.get(guild.roles, name='Member')
        if member_role in message.author.roles:
            await channel.send("Already verified.")
            return
        player = self.lwm_interface.get_player(message.content)
        if not player:
            return
        is_in_registered_clan = False
        for clan_id in player['clan_ids']:
            if str(clan_id) in self.servers_config[str(guild.id)]['clans']:
                is_in_registered_clan = True
                break
        if not is_in_registered_clan:
            await channel.send(
                    "Verification failed: " +
                    f"{player['name']} does not belong to one of the registered clans.")
            return
        try:
            await message.author.edit(nick=player['name'])
            await channel.send("Changed Discord nickname to match in-game name.")
        except Forbidden:
            pass
        try:
            await message.author.remove_roles(non_member_role)
            await message.author.add_roles(member_role)
        except Forbidden:
            pass
        await channel.send(f"{player['name']} have been verified.")

    @commands.command(name='set-verification-channel')
    @commands.has_permissions(manage_channels=True)
    async def set_verification_channel(self, context):
        "Assigns the bot to check for profile links in the specified channel."
        channel = context.message.channel
        guild = channel.guild
        category = None
        if channel.category_id:
            category = utils.get(guild.categories, id=channel.category_id)
        category_string = ""
        if category:
            category_string = f"{category.name}: "

        accepted_clans = []
        if str(guild.id) in self.servers_config:
            data = self.servers_config.pop(str(guild.id))
            accepted_clans = data['clans']
        self.servers_config[str(guild.id)] = {
                'server_name': guild.name,
                'category': {
                        'id': category.id if category else None,
                        'name': category.name if category else None},
                'channel': {
                        'id': channel.id,
                        'name': channel.name},
                'clans': accepted_clans}
        await context.channel.send(
                f"Listening for verification on {category_string}{channel.name}.")
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
        guild = context.message.channel.guild
        clans = {}
        if str(guild.id) in self.servers_config:
            clans = self.servers_config[str(guild.id)]['clans']
        if len(clans) == 0:
            await context.channel.send(
                    "There are currently no registered clans!\n" +
                    "Use the clan register command or type !help clan register.")
            return
        clans_string = "Registered clans:\n"
        for clan_id, clan in clans.items():
            clans_string += f"#{clan_id} {clan['name']}\n"
        await context.channel.send(clans_string)

    @clan.command(name='register', aliases=['add', 'new'])
    @commands.has_permissions(manage_channels=True)
    async def register_clan(self, context, clan):
        "Registers the specified clan to this discord server"
        new_clan = self.lwm_interface.get_clan(clan)
        if not new_clan:
            await context.channel.send(
                    f"Failed to find clan {clan}!\n" +
                    "Please specify a clan ID or link to a clan page.")
            return
        guild = context.message.channel.guild
        clans = {}
        if str(guild.id) in self.servers_config:
            clans = self.servers_config[str(guild.id)]['clans']
        else:
            self.servers_config[str(guild.id)] = {
                    'server_name': guild.name,
                    'clans': clans}
        if str(new_clan['id']) in clans:
            await context.channel.send(
                    f"Clan {new_clan['qualified_name']} have already been registered!\n" +
                    "Use the clan list command to check registered clans.")
            return
        self.servers_config[str(guild.id)]['clans'][str(new_clan['id'])] = {
                'name': new_clan['name']}
        await context.channel.send(
                f"Registered clan {new_clan['qualified_name']}.")
        await self.save_config()

    @clan.command(name='remove', aliases=['delete', 'del', 'rm'])
    @commands.has_permissions(manage_channels=True)
    async def remove_clan(self, context, clan):
        "Removes the specified clan from this discord server"
        old_clan = self.lwm_interface.get_clan(clan)
        if not old_clan:
            await context.channel.send(
                    f"Failed to find clan {clan}!\n" +
                    "Please specify a clan ID or link to a clan page.")
            return
        guild = context.message.channel.guild
        clans = {}
        if str(guild.id) in self.servers_config:
            clans = self.servers_config[str(guild.id)]['clans']
        if str(old_clan['id']) not in clans:
            await context.channel.send(
                    f"Clan {old_clan['qualified_name']} is not registered.")
            return
        self.servers_config[str(guild.id)]['clans'].pop(str(old_clan['id']))
        await context.channel.send(
                f"Removed clan {old_clan['qualified_name']}.")
        await self.save_config()

    @clan.error
    @list_clans.error
    @register_clan.error
    @remove_clan.error
    async def clan_error(self, context, error):
        # Normal users don't need to know that these commands exist.
        pass
