#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from discord.ext import commands

from persistence import PersistenceCog
from clan import ClanCog
from verification import VerificationCog


def main():
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(PersistenceCog(bot))
    bot.add_cog(ClanCog(bot))
    bot.add_cog(VerificationCog(bot))
    bot.run(token)


if __name__ == '__main__':
    main()
