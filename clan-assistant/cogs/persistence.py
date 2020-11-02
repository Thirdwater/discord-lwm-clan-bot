import os
import json
from discord.ext import commands


class Persistence(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.load_config()
        # print(self.bot.guilds)
        print(self.discord_config)
        print(self.members_record)

    async def get_clan_id(self):
        return self.discord_config['clan']['id']

    async def get_verification_channel(self):
        return self.discord_config['verification_channel']

    async def get_output_channel(self):
        return self.discord_config['output_channel']

    def load_config(self):
        self.discord_config_filename = os.getenv('DISCORD_CONFIG')
        self.members_record_filename = os.getenv('MEMBERS_RECORD')
        self.new_discord_config = {
                'clan': {
                        'id': None,
                        'name': None},
                'verification_channel': {
                        'id': None,
                        'name': None,
                        'category': {
                                'id': None,
                                'name': None}},
                'output_channel': {
                        'id': None,
                        'name': None,
                        'category': {
                                'id': None,
                                'name': None}}}
        self.discord_config = self.load_json(
                self.discord_config_filename, default=self.new_discord_config)
        self.new_members_record = []
        self.members_record = self.load_json(
                self.members_record_filename, default=self.new_members_record)
        
    async def save_json(self, filename, content):
        with open(filename, 'w', encoding='utf8') as json_file:
            json.dump(
                    content,
                    json_file,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4)

    def load_json(self, filename, default):
        if not os.path.isfile(filename):
            return default
        with open(filename) as json_file:
            return json.load(json_file)
