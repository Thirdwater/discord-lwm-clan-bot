import os
import json


class Persistence:
    
    def __init__(self):
        self.discord_config_filename = os.getenv('DISCORD_CONFIG')
        self.members_record_filename = os.getenv('MEMBERS_RECORD')
        self.load_config()

    async def get_main_clan_id(self):
        return self.discord_config['main_clan']['id']

    async def get_family_clan_ids(self):
        return self.discord_config['family_clans'].keys()

    async def set_verification_channel(self, channel):
        self.discord_config['verification_channel'] = channel

    async def get_verification_channel(self):
        return self.discord_config['verification_channel']

    async def set_output_channel(self, channel):
        self.discord_config['output_channel'] = channel

    async def get_output_channel(self):
        return self.discord_config['output_channel']

    async def save_config(self):
        await self.save_json(self.discord_config_filename, self.discord_config)
        await self.save_json(self.members_record_filename, self.members_record)
        print("    Saved discord config:")
        print(self.discord_config)
        print("    Saved members record:")
        print(self.members_record)

    def load_config(self):
        self.new_discord_config = {
                'main_clan': {
                        'id': None,
                        'name': None},
                'family_clans': {},
                'use_verification_code': False,
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
        print("    Loaded discord config:")
        print(self.discord_config)
        print("    Loaded members record:")
        print(self.members_record)
        
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
