#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from discord.ext import commands

from cogs import Persistence
from cogs import Clan
from cogs import Verification
from cogs import Log


def main():
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    
    bot = commands.Bot(command_prefix='!')

    bot.add_cog(Persistence(bot))
    bot.add_cog(Clan(bot))
    bot.add_cog(Verification(bot))
    bot.add_cog(Log(bot))

    bot.run(token)


if __name__ == '__main__':
    main()
