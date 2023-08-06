from discord.ext import commands as c
from discord import TextChannel, Embed, PermissionOverwrite, Role, utils
from asyncpgw import general
from datetime import datetime

import asyncio

#pylint: disable=import-error

from samep.cogs.utils import perms

paneru_table = """paneru(
    server bigint,
    paneru bigint,
    emoji text,
    bot_role bigint
)"""

nmatching_table = """nmatching(
    server bigint,
    channels bigint[]
)"""


class Paneru_(c.Cog, name="パネル"):
    def __init__(self, bot):
        self.bot = bot
        self.paneru = general.Pg(bot, 'paneru')
        self.nmatching = general.Pg(bot, 'nmatching')

    def cog_check(self, ctx):
        return ctx.guild.id in [754680802578792498, 594000178873237534]


    @c.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id is None:
            return
            
        if payload.member.bot:
            return 

        guild = self.bot.get_guild(payload.guild_id)
        channel = self.bot.get_channel(payload.channel_id)
        mes = await channel.fetch_message(payload.message_id)
        if (server := await self.paneru.fetch(server=payload.guild_id, paneru=payload.message_id)):
            await mes.remove_reaction(payload.emoji, payload.member)

            bot = guild.get_role(server['bot_role'])

            overwrites = {
                
                guild.default_role: PermissionOverwrite(read_messages=False),
                bot: PermissionOverwrite(read_messages=True),
                payload.member: PermissionOverwrite(read_messages=True),

            }

            if any(payload.member.display_name == channel.name for channel in guild.text_channels):
                return

            newc = await guild.create_text_channel(name=payload.member.display_name, overwrites=overwrites)
            
            await newc.send(f"{payload.member.mention}\nこのチャンネルは3分後自動で削除されます。")

            await asyncio.sleep(180)

            await newc.delete()