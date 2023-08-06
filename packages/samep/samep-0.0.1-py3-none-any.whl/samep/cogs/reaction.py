from discord.ext import commands as c
from discord import TextChannel, Embed, errors
from asyncpgw import general

#pylint: disable=import-error
from samep.cogs.utils import embed, paid, err

auto_reaction_table = """auto_reaction(
    server bigint,
    channel bigint,
    emojis text[] DEFAULT array[] :: text[]
)"""

class Auto_Reaction(c.Cog, name="リアクション"):
    def __init__(self, bot):
        self.bot = bot
        self.auto_reaction = general.Pg(bot, 'auto_reaction')


    @c.Cog.listener()
    @err.excepter
    async def on_message(self, mes):
        if not (server_data:= await self.auto_reaction.fetch(channel=mes.channel.id)):
            return

        for emoji in server_data['emojis']:
            
            try:
                await mes.add_reaction(emoji)
            except errors.HTTPException:
                pass


def setup(bot):
    bot.add_cog(Auto_Reaction(bot))
    bot.add_table(auto_reaction_table)