import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

guild_ids= [787773373748740128]
class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def _test(self, ctx: SlashContext):


def setup(bot):
    bot.add_cog(Slash(bot))