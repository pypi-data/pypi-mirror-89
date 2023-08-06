from discord.ext import commands as c
from discord import Embed, utils
from attrdict import AttrDict

class Dget:
    def __init__(self, bot):
        self.bot = bot


    async def text_channel(self, ctx, description=None):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        desc = description or '指定するテキストチャンネルを入力してね'

        await ctx.send(desc.replace('チャンネル', 'チャンネルの名前・ID・メンション'))


        get_channel = await self.bot.wait_for('message', check=check)

        try:
            channel = await c.TextChannelConverter().convert(ctx, get_channel.content)
            return channel
        except c.errors.ChannelNotFound:
            return None


    async def voice_channel(self, ctx, description=None):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        desc = description or '指定するボイスチャンネルを入力してね'

        await ctx.send(desc.replace('チャンネル', 'チャンネルの名前・ID・メンション'))

        get_channel = await self.bot.wait_for('message', check=check)

        try:
            channel = await c.VoiceChannelConverter().convert(ctx, get_channel.content)
            return channel
        except c.errors.ChannelNotFound:
            return None


    async def category_channel(self, ctx, description=None):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        desc = description or '指定するカテゴリーチャンネルを入力してね'

        await ctx.send(desc.replace('チャンネル', 'チャンネルの名前・ID・メンション'))

        get_channel = await self.bot.wait_for('message', check=check)

        try:
            channel = c.CategoryChannelConverter().convert(ctx, get_channel.content)
            return channel
        except c.errors.ChannelNotFound:
            return None

    async def role(self, ctx, description=None):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        desc = description or "指定する役職を入力してね"

        await ctx.send(desc.replace('役職', '役職の名前・ID・メンション'))

        get_role = await self.bot.wait_for('message', check=check)

        try:
            role = c.RoleConverter().convert(ctx, get_role.content)
            return role
        except c.errors.RoleNotFound:
            return None

    async def member(self, ctx, name, description=None):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        desc = description or '指定する人を入力してね'

        await ctx.send(desc.replace('人', '人の名前・ID・メンション'))

        get_member = await self.bot.wai_for('message', check=check)

        try:
            member = c.MemberConverter().convert(ctx, get_member.content)
            return member

        except c.errors.MemberNotFound:
            return None


    async def emoji_number(self, ctx, mes):
        def check(r, u):
            return ctx.author == u

        r, _u = await self.bot.wait_for('reaction_add', check=check)
        e = str(r.emoji)

        es = list(e)
        load_emoji = ctx.bot.get_emoji(773858253884227594)
      
        try:
            emoji = int(es[0])
            return emoji
        except ValueError:
            await mes.remove_reaction(load_emoji, self.bot.user)
            return None






    def ids(self):
        return AttrDict({
            "server": {
                "main": 754680802578792498
            },
            "channels": {
                "male": 767307773553672212,
                "female": 767307843056435240,
                "profile_notice": 773204984899829760,
                "server_update": 767375108636934184,
                "bot_update": 767375135547064381,
                "greeting": 767339917659209761,
                "err": 754710116753997876,
                "paid": 764394104431181824,
                "open_ban": 767404090908475432
            },
            "roles": {
                "male": 755080619637080225,
                "female": 755087406335524945,
                "not_profile": 767337793504280637,
                "greeting": 767340587162402818
            }
        })
            