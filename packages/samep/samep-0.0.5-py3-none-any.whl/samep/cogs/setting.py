from discord.ext import commands as c
from discord import Embed, utils, errors, PermissionOverwrite, Colour, TextChannel
from asyncpgw import general
from datetime import datetime
from asyncio import create_task, wait, FIRST_COMPLETED

import re, importlib

# pylint: disable=import-error
from samep.cogs.utils import embed, dget


class Setting(c.Cog, name="設定"):
    def __init__(self, bot):
        self.bot = bot
        
        self.auto_reaction = general.Pg(bot, 'auto_reaction')
        self.base_matching = general.Pg(bot, 'base_matching')
        self.base_role_ = general.Pg(bot, 'base_role')
        self.matching = general.Pg(bot, 'matchi')
        self.paneru = general.Pg(bot, 'paneru')

        importlib.reload(embed)
        importlib.reload(dget)
        self.dget = dget.Dget(bot)


    async def load(self):
        import aiofiles, json
        async with aiofiles.open("select.json") as f:
            data = await f.read()
            return json.loads(data)


    @c.command(hidden=True)
    async def smat(self, ctx):
        "マッチングの設定"

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        if not await self.base_role_.fetch(server=ctx.guild.id):
            await self.base_role_.insert(server=ctx.guild.id)

        data = await self.load()


        default_mes, load_emoji = await embed.select(ctx, data["matching"])


        while True:
            emoji = await self.dget.emoji_number(ctx, default_mes)

            if emoji is None:
                continue

            if emoji == 4:
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)
                

            elif emoji == 1:
                role = await self.dget.role(ctx)

                if role is None:
                    e = embed.error('役職が見つからなかったよ')
                    return await ctx.send(embed=e)

                await self.base_role_.update(base_boy_role=role.id, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["matching"])

            elif emoji == 2:
                role = await self.dget.role(ctx)

                if role is None:
                    e = embed.error('役職が見つからなかったよ')
                    return await ctx.send(embed=e)

                await self.base_role_.update(base_girl_role=role.id, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["matching"])

            elif emoji == 3:
                await ctx.send('パネルの説明を入力してね')

                pdesc = await self.bot.wait_for('message', check=check)

                e = embed.succes(desc=pdesc.content)
                mes = await ctx.send(embed=e)

                await ctx.send('`登用用の絵文字` `編集用の絵文字` `削除用の絵文字`を入力してね')

                eme = await self.bot.wait_for('message', check=check)
                emoji_list = list(eme.content)
                emojis = [emoji for emoji in emoji_list if emoji != ' ']

                await mes.add_reaction(emojis[0].replace(' ', ''))
                await mes.add_reaction(emojis[1].replace(' ', ''))
                await mes.add_reaction(emojis[2].replace(' ', ''))

                await ctx.send('テンプレートを入力してね')

                template = await self.bot.wait_for('message', check=check)

                await ctx.send('通知を飛ばす男性についてる役職を選択してね')

                boyrole = await self.dget.role(ctx)

                if boyrole is None:
                    e = embed.error('役職が見つからなかったよ')
                    return await ctx.send(embed=e)

                await ctx.send('通知を飛ばす女性についてる役職を選択してね')

                girlrole = await self.dget.role(ctx)

                if girlrole is None:
                    e = embed.error('役職が見つからなかったよ')
                    return await ctx.send(embed=e)

                await ctx.send('男性の投稿文を送信するテキストチャンネルを選択してね')

                boychannel = await self.dget.text_channel(ctx)

                if boychannel is None:
                    e = embed.error('役職が見つからなかったよ')
                    return await ctx.send(embed=e)

                await ctx.send('女性の投稿文を送信するテキストチャンネルを送信してね')

                girlchannel = await self.dget.text_channel(ctx)

                if girlchannel is None:
                    e = embed.error('チャンネルが見つからなかったよ')
                    return await ctx.send(embed=e)

                await self.base_matching.insert(
                    server=ctx.guild.id,
                    paneru_mes=mes.id,
                    boy_channel=boychannel.id,
                    girl_channel=girlchannel.id,
                    template=template.content,
                    boy_role=boyrole.id,
                    girl_role=girlrole.id,
                    post_emoji=emojis[0],
                    edit_emoji=emojis[1],
                    del_emoji=emojis[2])

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["matching"])

            else:
 
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)

    @c.command(hidden=True)
    async def smoment(self, ctx):
        "一時テキストチャンネルを作るパネルを設定"

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        if not await self.paneru.fetch(server=ctx.guild.id):
            await self.paneru.insert(server=ctx.guild.id)

        await ctx.send('パネルの説明文を入力してね')
        panerudesc = await self.bot.wait_for('message', check=check)

        e = embed.succes(desc=panerudesc.content)
        mes = await ctx.send(embed=e)

        await ctx.send('パネルにつけるリアクションの絵文字を入力してね')

        emoji = await self.bot.wait_for('message', check=check)
        await mes.add_reaction(emoji.content)

        await self.paneru.update(paneru=mes.id, server=ctx.guild.id)
       

        e = embed.succes(desc="処理が正常に終了したよ")
        await ctx.send(embed=e)


    @c.command()
    async def sre(self, ctx):
        "自動リアクションをする設定"

        def check(m):
            return ctx.author == m.author and m.channel == ctx.channel

        await ctx.send('リアクションを自動で追加するチャンネルを選択してね')

        channel = await self.dget.text_channel(ctx)

        if channel is None:
            e = embed.error('チャンネルが見つからなかったよ')
            return await ctx.send(embed=e)

        await ctx.send('つける絵文字を入力してね。複数指定できるよ')

        e = await self.bot.wait_for('message', check=check)

        if not (channel_data := await self.auto_reaction.fetch(channel=channel.id)):
            await self.auto_reaction.insert(channel=channel.id)

        custom_emojis = re.findall(r'(<a?:\w+:\d+>)', e.content)

        for emoji in custom_emojis:
            if channel_data is None:
                await self.auto_reaction.add(emojis=emoji, channel=channel.id)
                continue

            if emoji not in channel_data['emojis']:
                await self.auto_reaction.add(emojis=emoji, channel=channel.id)

        import emojis

        emojii = emojis.get(e.content)

        for emoji in emojii:

            if channel_data is None:
                await self.auto_reaction.add(emojis=emoji, channel=channel.id)
                continue

            if emoji not in channel_data['emojis']:
                await self.auto_reaction.add(emojis=emoji, channel=channel.id)

        e = embed.succes(desc="処理が正常に終了したよ")
        await ctx.send(embed=e)


    @c.command()
    async def dsre(self, ctx, channel: TextChannel=None):
        if channel is None:
            channel = ctx.channel

        if not await self.auto_reaction.fetch(channel=channel.id):
            e = embed.error('チャンネルデータが見つからなかったよ')
            return await ctx.send(embed=e)

        else:
            await self.auto_reaction.delete(channel=channel.id)
            e = embed.succes(desc=f"{channel.mention}のデータを削除したよ")
            return await ctx.send(embed=e)
