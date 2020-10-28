import os
import json
from discord.ext import commands


class PersistenceCog(commands.Cog, name="Persistence"):
    
    def __init__(self, bot):
        self.bot = bot
        self.load_config()

    @commands.group(name='get', invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def get(self, context):
        "Displays the current discord configurations"
        await context.send_help(context.command)

    @get.command(name='verification_channel')
    @commands.has_permissions(manage_channels=True)
    async def get_verification_channel(self, context):
        ""
        pass

    @get.command(name='output_channel')
    @commands.has_permissions(manage_channels=True)
    async def get_output_channel(self, context):
        ""
        pass

    def load_config(self):
        self.discord_config_filename = os.getenv('DISCORD_CONFIG')
        self.members_record_filename = os.getenv('MEMBERS_RECORD')
        
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
