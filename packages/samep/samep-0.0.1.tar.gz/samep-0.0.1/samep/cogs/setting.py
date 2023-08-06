from discord.ext import commands as c
from discord import Embed, utils, errors, PermissionOverwrite, Colour, TextChannel
from asyncpgw import general
from datetime import datetime
from asyncio import create_task, wait, FIRST_COMPLETED

import re, importlib

# pylint: disable=import-error
from samep.cogs.utils import embed, dget, paid

prefix_table = """prefix(
    server bigint,
    prefixes text[] DEFAULT array[]::text[]
)"""


class Setting(c.Cog, name="設定"):
    def __init__(self, bot):
        self.bot = bot
        
        self.plan = paid.Plan(bot)
        self.anony = general.Pg(bot, 'anony')
        self.auto_channel = general.Pg(bot, 'auto_channel')
        self.auto_reaction = general.Pg(bot, 'auto_reaction')
        self.auto_delete = general.Pg(bot, 'auto_delete')
        self.bump = general.Pg(bot, 'bump')
        self.moveer = general.Pg(bot, 'moveer')
        self.profile = general.Pg(bot, 'profile')
        self.logs = general.Pg(bot, 'logs')
        self.spam = general.Pg(bot, 'spam')
        self.reaction_role = general.Pg(bot, 'reaction_role')
        self.base_matching = general.Pg(bot, 'base_matching')
        self.base_role_ = general.Pg(bot, 'base_role')
        self.matching = general.Pg(bot, 'matchi')
        self.paneru = general.Pg(bot, 'paneru')
        self.prefix = general.Pg(bot, 'prefix')
        self.stats = general.Pg(bot, 'stats')
        self.ut = general.Pg(bot, 'user_time')
        self.bc = general.Pg(bot, 'black_channel')
        self.wc = general.Pg(bot, 'white_channel')
        self.insider = general.Pg(bot, 'insider')
        self.tv = general.Pg(bot, 'text_voice')
        self.real_time = general.Pg(bot, "real_time_log")
        self.real_time_limit = general.Pg(bot, "real_time_limit")

        importlib.reload(embed)
        importlib.reload(dget)
        importlib.reload(paid)
        self.dget = dget.Dget(bot)

    


    async def load(self):
        import aiofiles, json
        async with aiofiles.open("select.json") as f:
            data = await f.read()
            return json.loads(data)



    async def check_reactions(self, ctx, description):
        def react_check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['⭕', '❌']

        e = Embed(
            description=description
        )
        e.set_author(name='`⭕❌`で選択してね')
        m = await ctx.send(embed=e)
        await m.add_reaction("⭕")
        await m.add_reaction('❌')

        reaction, _user = await self.bot.wait_for('reaction_add', check=react_check)

        return reaction

    async def get_paneru(self, channel, title):
        async for mes in channel.history():
            if not (embed := mes.embeds):
                continue

            for e in embed:
                try:
                    if title in e.author.name:
                        return e, mes
                except TypeError:
                    continue

    async def get_new_channel(self, payload, guild, data):

        channel = self.bot.get_channel(payload.channel_id)

        overwrites = {
            guild.default_role: PermissionOverwrite(read_messages=False),
            guild.me: PermissionOverwrite(read_messages=True),
            payload.member: PermissionOverwrite(read_messages=True)
        }

        if any(c.name == payload.member.display_name for c in guild.text_channels):
            new_channel = utils.get(
                guild.text_channels, name=payload.member.display_name)

        else:
            new_channel = await channel.category.create_text_channel(name=payload.member.display_name, overwrites=overwrites, position=0)

        temp = await self.base_matching.fetch(paneru_mes=payload.message_id, post_emoji=str(payload.emoji))
        if temp is not None:
            await new_channel.send(f"{payload.member.mention}\n{data['post_emoji']}こちらは代理投稿用の記入画面です。\n下記のテンプレートを使用し、募集文を投稿してください。\n:warning:このチャンネルは５分後自動的に消滅します。\n\n　 　↓　↓ テンプレート ↓　↓")
            await new_channel.send(temp['template'])
            return new_channel

        else:
            temp = await self.base_matching.fetch(paneru_mes=payload.message_id, edit_emoji=str(payload.emoji))
            await new_channel.send(f"{payload.member.mention}\n{data['edit_emoji']}こちらは代理編集用の記入画面です。\n下記のテンプレートを使用し、募集文を編集してください。\n:warning:このチャンネルは５分後自動的に消滅します。\n\n　 　↓　↓ テンプレート ↓　↓")
            await new_channel.send(temp['template'])
            return new_channel

    async def check_anony_react(self, mes, content):
        if '匿名リアクション' in content:
            await mes.add_reaction('\U0000270b')
            await mes.add_reaction('\U0000274e')

        else:
            await mes.clear_reactions()

    async def check_recruit(self, opt, member, channel, base_data, data):
        base_role = await self.base_role_.fetch(server=member.guild.id)
        boy_role = member.guild.get_role(base_role['base_boy_role'])
        girl_role = member.guild.get_role(base_role['base_girl_role'])

        if boy_role in member.roles:
            c = self.bot.get_channel(base_data['boy_channel'])
        elif girl_role in member.roles:
            c = self.bot.get_channel(base_data['girl_channel'])

        try:
            if opt == "send":
                await c.fetch_message(data['mes'])
                e = embed.error(
                    f'既に{str(c)}で募集をしています。募集を新たにしたい場合は、{channel.mention}の:wastebasket:を押して、前回の募集を削除してください。')
                return await member.send(embed=e)

            else:
                e = embed.error(f'【{str(c)}】にあなたの投稿文は見つかりませんでした。')
            await member.send(embed=e)
        except errors.NotFound:
            user_datas = await self.matching.fetchs(member=member.id)
            for user_data in user_datas:
                await self.matching.delete(mes=user_data['mes'], member=member.id)

            e = Embed(
                title=str(member),
                description="データの消去をしました"
            )
            e.set_footer(
                text=f"《削除日時》{datetime.now().strftime('%m月%d日%H時%M分')}\n{channel.guild.name}")

            await self.bot.get_channel(772406361819971604).send(embed=e)

    async def check_role(self, payload, member, guild, emoji, base_data):
        paneru_data = await self.base_matching.fetch(paneru_mes=payload.message_id, post_emoji=str(payload.emoji))
        if paneru_data is None:
            paneru_data = await self.base_matching.fetch(paneru_mes=payload.message_id, edit_emoji=str(payload.emoji))
            if paneru_data is None:
                paneru_data = await self.base_matching.fetch(paneru_mes=payload.message_id, del_emoji=str(payload.emoji))

        base_role = await self.base_role_.fetch(server=member.guild.id)

        boy_role = guild.get_role(base_role['base_boy_role'])
        girl_role = guild.get_role(base_role['base_girl_role'])

        if boy_role in member.roles and girl_role in member.roles:
            e = embed.error(
                f'貴方には{str(boy_role)}・{str(girl_role)}２つの役職がついてつため、募集をすることが出来ません。')
            await member.send(embed=e)

            role = None
            requchannel = None
            colour = None

        elif boy_role in member.roles:
            role = guild.get_role(base_data['girl_role'])
            requchannel = self.bot.get_channel(base_data['boy_channel'])
            colour = Colour.blue()

        elif girl_role in member.roles:
            role = guild.get_role(base_data['boy_role'])
            requchannel = self.bot.get_channel(base_data['girl_channel'])
            colour = Colour.red()

        else:
            e = embed.error(
                f'貴方には{str(boy_role)}・{str(girl_role)}どちらかの役職が付いて居ないため募集をすることが出来ません。')
            await member.send(embed=e)

            role = None
            requchannel = None
            colour = None

        return role, requchannel, colour

    async def send_embed(self, payload, m, emoji, base_data):
        role, target, colour = await self.check_role(payload, m.author, m.guild, emoji, base_data)

        if role is None:
            requmes = None
            return requmes

        e = Embed(
            description=m.content,
            colour=colour
        )
        e.set_author(name=m.author.display_name, icon_url=m.author.avatar_url)
        e.set_thumbnail(url=m.author.avatar_url)
        e.set_footer(text=f"{str(m.author)} | {m.author.id}")
        requ_mes = await target.send(role.mention, embed=e)
        await self.check_anony_react(requ_mes, m.content)
        return requ_mes

    async def edit_embed(self, payload, m, content, emoji, base_data, data):
        role, target, colour = await self.check_role(payload, m, m.guild, emoji, base_data)

        mes = await target.fetch_message(data['mes'])

        if role is None:
            requmes = None
            return requmes

        e = Embed(
            description=content,
            colour=colour
        )
        e.set_author(name=m.display_name, icon_url=m.avatar_url)
        e.set_thumbnail(url=m.avatar_url)
        e.set_footer(text=f"{str(m)} | {m.id}")
        requ_mes = await mes.edit(content=role.mention, embed=e)
        await self.check_anony_react(mes, content)
        return requ_mes

    async def send_poster(self, payload, requmes, base_data):
        mm = self.bot.get_channel(payload.channel_id)
        _role, _channel, colour = await self.check_role(payload, payload.member, mm.guild, payload.emoji, base_data)
        e = Embed(
            title=f"{base_data['post_emoji']} 代理投稿完了 {base_data['post_emoji']}",
            description=f"{requmes.content}\n編集削除は{mm.mention}の{base_data['edit_emoji']}{base_data['del_emoji']}ボタンを押してください。",
            colour=colour
        )

        e.set_footer(
            text=f"《投稿日時》{datetime.now().strftime('%m月%d日%H時%M分')}\n{mm.guild.name} / {mm.name}")

        e_m = await payload.member.send(embed=e)

        return e_m

    async def send_editer(self, payload, requmes, base_data):
        mm = self.bot.get_channel(payload.channel_id)
        _role, channel, colour = await self.check_role(payload, payload.member, mm.guild, payload.emoji, base_data)

        e = Embed(
            title=f"{base_data['edit_emoji']} 編集処理完了 {base_data['edit_emoji']}",
            description=f"{requmes.content}\n編集削除は{mm.mention}の{base_data['edit_emoji']}{base_data['del_emoji']}ボタンを押してください。",
            colour=colour
        )

        e.set_footer(
            text=f"《投稿日時》{datetime.now().strftime('%m月%d日%H時%M分')}\n{channel.guild.name} / {channel.name}")

        e_m = await payload.member.send(embed=e)

        return e_m

    async def send_deleter(self, payload, base_data):
        guild = self.bot.get_guild(payload.guild_id)
        _role, channel, colour = await self.check_role(payload, payload.member, guild, payload.emoji, base_data)
        e = Embed(
            title=f"{base_data['del_emoji']} 削除処理完了 {base_data['del_emoji']}",
            colour=colour
        )

        e.set_footer(
            text=f"《投稿日時》{datetime.now().strftime('%m月%d日%H時%M分')}\n{channel.guild.name} / {channel.name}")

        e_m = await payload.member.send(embed=e)

        return e_m

    @c.command()
    async def sa(self, ctx):
        """匿名でメッセージを送信する設定"""

        await ctx.send('パネルを作成するチャンネルの名前を入力してね')

        channel = await self.dget.text_channel(ctx)

        if channel is None:
            e = embed.error('指定されたチャンネルは見つからなかったよ。')
            return await ctx.send(embed=e)

        if not (webhook := utils.get(await channel.webhooks(), name="same匿名")):
            webhook = await channel.create_webhook(name="same匿名")

        webhook_url = webhook.url

        e = Embed(
            description="匿名で送信するメッセージを入力するためのチャンネルを作成するパネルを作成するよ"
        )
        e.set_author(name="パネルを反応させる絵文字を送信してね")
        await ctx.send(embed=e)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        set_emoji = await self.bot.wait_for('message', check=check)

        e = Embed(
            description="下のリアクションを押すと匿名メッセージを書き込むチャンネルが作成されるよ"
        )
        m = await ctx.send(embed=e)

        try:
            await m.add_reaction(set_emoji.content)
        except errors.HTTPException:
            e = embed.error('絵文字が見つからなかったよ')
            return await ctx.send(embed=e)

        e = Embed(
            description="匿名でメッセージを送信する時のユーザーの名前を入力してね"
        )
        await ctx.send(embed=e)

        username = await self.bot.wait_for('message', check=check)

        await ctx.send('匿名メッセージを送信した時にメンションする？ `する`か`しない`で答えてね。')

        check_mention = await self.bot.wait_for('message', check=check)

        if check_mention.content not in ['y', 'Y', 'はい', 'は', 'する', 'す']:
            role = 00000

        else:
            await ctx.send('下の中からメンションする役職を選択してね')

            role = await self.dget.role(ctx)

            if role is None:
                e = embed.error('指定された役職は見つからなかったよ')
                return await ctx.send(embed=e)

            role = role.id

        await self.anony.insert(server=ctx.guild.id, input_paneru=m.id, output_channel=webhook_url, mrole=role, name=username.content)

        e = embed.succes(desc="処理が正常に終了したよ")
        return await ctx.send(embed=e)

    @c.command()
    async def sb(self, ctx):
        """bumpの設定"""

        if not await self.bump.fetch(server=ctx.guild.id):
            await self.bump.insert(server=ctx.guild.id)

        data = await self.load()

        default_mes, load_emoji = await embed.select(ctx, data['bump'])

        while True:
            emoji = await self.dget.emoji_number(ctx, default_mes)

            if emoji is None:
                continue

            if emoji == 7:
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)
            
            elif emoji == 1:
                reaction = await self.check_reactions(ctx, '通知を有効にする？')

                if str(reaction.emoji) == "⭕":
                    await self.bump.update(enable=True, server=ctx.guild.id)
                else:
                    await self.bump.update(enable=False, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)
                default_mes, load_emoji = await embed.select(ctx, data['bump'])

            elif emoji == 2:
                reaction = await self.check_reactions(ctx, '深夜の通知を有効にする？')

                if str(reaction.emoji) == "⭕":
                    await self.bump.update(night_enable=True, server=ctx.guild.id)
                else:
                    await self.bump.update(night_enable=False, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)
                default_mes, load_emoji = await embed.select(ctx, data['bump'])

            elif emoji == 3:
                await ctx.send('下の中からメンションする役職を選択してね')

                role = await self.dget.role(ctx)

                if role is None:
                    e = embed.error('役職は見つからなかったよ')
                    return await ctx.send(embed=e)

                await self.bump.update(role=role.id, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)
                default_mes, load_emoji = await embed.select(ctx, data['bump'])

            elif emoji == 4:
                await ctx.send('下の中から深夜にメンションする役職を選択してね')

                role = await self.dget.role(ctx)

                if role is None:
                    e = embed.error('役職は見つからなかったよ')
                    return await ctx.send(embed=e)

                await self.bump.update(night_role=role.id, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)
                default_mes, load_emoji = await embed.select(ctx, data['bump'])

            elif emoji == 5:
                reaction = await self.check_reactions(ctx, 'メンションを有効にする？')

                if str(reaction.emoji) == "⭕":
                    await self.bump.update(mention=True, server=ctx.guild.id)
                else:
                    await self.bump.update(mention=False, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)
                default_mes, load_emoji = await embed.select(ctx, data['bump'])

            elif emoji == 6:
                reaction = await self.check_reactions(ctx, '深夜メンションを有効にする？')

                if str(reaction.emoji) == "⭕":
                    await self.bump.update(night_mention=True, server=ctx.guild.id)
                else:
                    await self.bump.update(night_mention=False, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)
                default_mes, load_emoji = await embed.select(ctx, data['bump'])

            else:
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)

    @c.command()
    async def channel(self, ctx):
        "チャンネルの自動追加の設定"

        data = await self.load()

        default_mes, load_emoji = await embed.select(ctx, data["channel"])

        while True:
            emoji = await self.dget.emoji_number(ctx, default_mes)

            if emoji is None:
                continue

            if emoji == 5:
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)
                

            elif emoji == 1:
                quantity = await self.auto_channel.fetchs(server=ctx.guild.id)
                if len(quantity) >= 4:
                    if self.plan.check_plan(ctx.guild, ctx.author):
                        return await self.plan.send_paid(ctx)

                m, load_emoji = await embed.select_opt(ctx, "フリーチャンネル,2shot,個室,隠れ個室,椅子,キャンセル")

                emoji_ = await self.dget.emoji_number(ctx, m)

                if emoji_ is None:
                    continue

                if emoji_ == 1:
                    opt = 'free'
                elif emoji_ == 2:
                    opt = 'two_shot'
                elif emoji_ == 3:
                    opt = 'private'
                elif emoji_ == 4:
                    opt = 'secret_private'
                elif emoji_ == 5:
                    opt = 'isu'
                elif emoji_==6:
                    await default_mes.remove_reaction(load_emoji, self.bot.user)
                    e = embed.succes(desc="キャンセルしたよ")
                    return await ctx.send(embed=e)
                
                channel = await self.dget.voice_channel(ctx)

                if channel is None:
                    e = embed.error('チャンネルは見つからなかったよ')
                    return await ctx.send(embed=e)

                if not await self.auto_channel.fetch(server=ctx.guild.id, voice_channel=channel.id):
                    await self.auto_channel.insert(server=ctx.guild.id, voice_channel=channel.id, option=opt, category_channel=channel.category.id)

                else:
                    await self.auto_channel.update(voice_channel=channel.id, server=ctx.guild.id)
                    await self.auto_channel.update(category_channel=channel.category.id, server=ctx.guild.id, voice_channel=channel.id)
                    await self.auto_channel.update(option=opt, server=ctx.guild.id, voice_channel=channel.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data['channel'])

            elif emoji == 2:
                channel = await self.dget.voice_channel(ctx)

                if channel is None:
                    e = embed.error('チャンネルは見つからなかったよ')
                    return await ctx.send(embed=e)

                if not await self.auto_channel.fetch(server=ctx.guild.id, voice_channel=channel.id):
                    e = embed.error('そのチャンネルのデータに存在しません')
                    return await ctx.send(embed=e)

                await self.auto_channel.delete(server=ctx.guild.id, voice_channel=channel.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data['channel'])

            elif emoji == 3:
                role = await self.dget.role(ctx)

                if role is None:
                    e = embed.error('役職は見つからなかったよ')
                    return await ctx.send(embed=e)

                await self.auto_channel.add(user_role=role.id, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data['channel'])

            elif emoji == 4:
                role = await self.dget.role(ctx)

                if role is None:
                    e = embed.error('役職は見つからなかったよ')
                    return await ctx.send(embed=e)

                await self.auto_channel.add(bot_role=role.id, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data['channel'])

            else:
             
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)

    @c.command()
    async def sd(self, ctx):
        "自動削除の設定"

        def check(m):
            return ctx.author == m.author and m.channel == ctx.channel

        data = await self.load()

        default_mes, load_emoji = await embed.select(ctx, data["delete"])

        while True:
            emoji = await self.dget.emoji_number(ctx, default_mes)

            if emoji is None:
                continue

            if emoji==4:
               
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)
                

            elif emoji == 1:

                channel = await self.dget.text_channel(ctx)

                if channel is None:
                    e = embed.error('チャンネルは見つからなかったよ')
                    return await ctx.send(embed=e)

                e = Embed(
                    title="どのくらいの期間で消しますか？",
                    description="例:)\n1ヶ月の場合 -> 1月\n2週間の場合 -> 2週\n３日の場合 -> 3日"
                )

                await ctx.send(embed=e)

                m = await self.bot.wait_for('message', check=check)

                if m.content in "月" and m.content in "週" and m.content in "日":
                    return await ctx.send('不正な文字が入力されました。')

                elif "月" in m.content:
                    option = "m"

                elif "週" in m.content:
                    option = "w"
                elif "日" in m.content:
                    option = "d"

                else:
                    return await ctx.send('不正な文字が入力されました。')

                period = int(re.sub("\\D", "", m.content))

                if not await self.auto_delete.fetch(server=ctx.guild.id, channel=channel.id):
                    await self.auto_delete.insert(server=ctx.guild.id, channel=channel.id, opt=option, period=period)

                else:
                    await self.auto_delete.update(opt=option, server=ctx.guild.id, channel=channel.id)
                    await self.auto_delete.update(period=period, server=ctx.guild.id, channel=channel.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["delete"])

            elif emoji == 2:
                channel = await self.dget.text_channel(ctx)

                if channel is None:
                    e = embed.error('チャンネルは見つからなかったよ')
                    return await ctx.send(embed=e)

                if await self.auto_delete.fetch(server=ctx.guild.id, channel=channel.id):
                    await self.auto_delete.delete(server=ctx.guild.id, channel=channel.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["delete"])

            elif emoji == 3:
                datas = await self.auto_delete.fetchs(server=ctx.guild.id)

                ed = [
                    f"{i}->{data['period']}{data['opt']}: {self.bot.get_channel(data['channel']).mention}" for i, data in enumerate(datas, 1)]

                e = embed.succes(
                    desc='\n'.join(ed)
                )
                await ctx.send(embed=e)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["delete"])

            else:
              
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)

    @c.command()
    async def slog(self, ctx):
        "ログを設定"

        data = await self.load()

        default_mes, load_emoji = await embed.select(ctx, data["log"])

        emoji = await self.dget.emoji_number(ctx, default_mes)

        if emoji is None:
            return

        if emoji == 1:
            option = "channel"
            goption = "チャンネルの作成・削除"
        elif emoji == 2:
            option = "ban"
            goption = "BAN"
        elif emoji == 3:
            option = "member"
            goption = "メンバーの入退出"
        elif emoji == 4:
            option = "vc"
            goption = "VCの入退出"
        elif emoji == 5:
            option = "mes"
            goption = "メッセージの編集・削除"

        await ctx.send("下の中からログを流すチャンネルを選択してね")


        channel = await self.dget.text_channel(ctx)
        if channel is None:
            e = embed.error(f'1 ~ {len(ctx.guild.text_channels)}番の中から番号を入力してね。コマンドの入力からやり直してね')
            return await ctx.send(embed=e)

        e = Embed(
            description=f"{goption}\nログ出力チャンネル -> {channel.mention}"
        )
        reaction = await self.check_reactions(ctx, 'この設定で良い？')

        if str(reaction.emoji) == "❌":
            e = embed.error('キャンセルされました')
            return await ctx.send(embed=e)

        if not (data := await self.logs.fetch(server=ctx.guild.id, option=option)):
            await self.logs.insert(server=ctx.guild.id, option=option, channel=channel.id)

        else:
            if data['option'] != option:
                await self.logs.update(option=option, server=ctx.guild.id)
            if data['channel'] != channel.id:
                await self.logs.update(channel=channel.id, server=ctx.guild.id, option=option)

        await default_mes.remove_reaction(load_emoji, self.bot.user)

        e = embed.succes(title="保存に成功したよ", desc=f"オプション->{goption}")
        await ctx.send(embed=e)

    @c.command()
    async def smc(self, ctx):
        "一般ユーザーと管理者を飛ばすVCを設定"
        await ctx.send('下に表示されてるチャンネル一覧から`管理者`を飛ばすVCを選択してね')

        channel = await self.dget.voice_channel(ctx)

        if channel is None:
            e = embed.error('チャンネルが見つかりませんでした。')
            return await ctx.send(embed=e)

        if not await self.moveer.fetch(server=ctx.guild.id):
            await self.moveer.insert(server=ctx.guild.id)

        await self.moveer.update(admin_channel=channel.id, server=ctx.guild.id)

        await ctx.send('下に表示されてるチャンネル一覧から`一般ユーザー`を飛ばすVCを選択してね')

        channel = await self.dget.voice_channel(ctx)

        if channel is None:
            e = embed.error('チャンネルが見つかりませんでした。')
            return await ctx.send(embed=e)

        await self.moveer.update(general_channel=channel.id, server=ctx.guild.id)

        e = embed.succes(desc="処理が正常に終了したよ")
        return await ctx.send(embed=e)

    @c.command()
    async def spr(self, ctx):
        """プロフィールに関する設定"""

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        if not await self.profile.fetch(server=ctx.guild.id):
            await self.profile.insert(server=ctx.guild.id)

        data = await self.load()

        default_mes, load_emoji = await embed.select(ctx, data["profile"])

        while True:
            emoji = await self.dget.emoji_number(ctx, default_mes)

            if emoji is None:
                continue

            if emoji == 6:
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)
                

            elif emoji == 1:
                channel = await self.dget.text_channel(ctx)

                if channel is None:
                    e = embed.error('チャンネルが見つからなかったよ')
                    return await ctx.send(embed=e)

                await self.profile.update(male_channel=channel.id, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)
                default_mes, load_emoji = await embed.select(ctx, data["profile"])

            elif emoji == 2:
                channel = await self.dget.text_channel(ctx)

                if channel is None:
                    e = embed.error('チャンネルが見つからなかったよ')
                    return await ctx.send(embed=e)

                await self.profile.update(female_channel=channel.id, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["profile"])

            elif emoji == 3:
                channel = await self.dget.text_channel(ctx)

                if channel is None:
                    e = embed.error('チャンネルが見つからなかったよ')
                    return await ctx.send(embed=e)

                    

                await self.profile.update(send_channel=channel.id, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)
                default_mes, load_emoji = await embed.select(ctx, data["profile"])

            elif emoji == 4:
                e = Embed(
                    description='チェックする単語を`|`で区切って指定してね'
                )
                e.set_author(name='一つの場合は単語だけでいいよ！')
                e.set_footer(text='↓↓↓↓コピペ用↓↓↓↓')
                await ctx.send(embed=e)
                await ctx.send('|')

                im = await self.bot.wait_for('message', check=check)

                iml = im.split('|')

                for word in iml:
                    await self.profile.add(words=word, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["profile"])

            elif emoji == 5:
                e = Embed(
                    description='チェックする単語を削除するよ！ `|`で区切って指定してね'
                )
                e.set_author(name='一つの場合は単語だけでいいよ！')
                e.set_footer(text='↓↓↓↓コピペ用↓↓↓↓')
                await ctx.send(embed=e)
                await ctx.send('|')

                im = await self.bot.wait_for('message', check=check)

                iml = im.split('|')

                for word in iml:
                    await self.profile.remove(words=word, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["profile"])

            else:
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)

    @c.command()
    async def snm(self, ctx):
        "メンションを禁止の設定"

        def check(m):
            return ctx.author == m.author and m.channel == ctx.channel

        if not await self.spam.fetch(server=ctx.guild.id):
            await self.spam.insert(server=ctx.guild.id)

        data = await self.load()


        default_mes, load_emoji = await embed.select(ctx, data["notmention"])

        while True:
            emoji = await self.dget.emoji_number(ctx, default_mes)

            if emoji is None:
                continue

            if emoji == 3:
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)
                

            elif emoji == 1:

                channel = await self.dget.text_channel(ctx)

                if channel is None:
                    e = embed.error('チャンネルが見つからなかったよ')
                    return await ctx.send(embed=e)

                if not await self.spam.fetch(sever=ctx.guild.id, channel=channel.id):
                    await self.spam.insert(server=ctx.guild.id, channel=channel.id)

                else:
                    await self.spam.update(channel=channel.id, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["notmention"])

            elif emoji == 2:

                e = Embed(description="メンションされた時に流すメッセージを入力してね")
                await ctx.send(embed=e)

                mes = await self.bot.wait_for('message', check=check)

                await self.spam.update(custom_message=mes.content, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["notmention"])

            else:
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)

    @c.command()
    async def srr(self, ctx):
        "リアクションロールの設定"
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        data = await self.load()


        default_mes, load_emoji = await embed.select(ctx, data["reactionrole"])

        while True:
            emoji = await self.dget.emoji_number(ctx, default_mes)

            if emoji is None:
                continue

            if emoji == 5:
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)
                

            elif emoji == 1:


                await ctx.send('パネルのタイトルを入力してね')
                title = await self.bot.wait_for('message', check=check)

                await ctx.send('パネルの説明を入力してね | 不要なときは`キャンセル`と入力してね')
                desc = await self.bot.wait_for('message', check=check)
                while True:
                    await ctx.send("役職と絵文字の設定をします。\n設定する役職と絵文字を\n:one: @AAA\n:two: @BBB\nという形で入力してね。\n入力した文章がそのままパネルに表示されるよ。")

                    paneru_ = await self.bot.wait_for('message', check=check)

                    paneru = paneru_.content

                    m = await ctx.send('役職と絵文字に間違いはない？')

                    await m.add_reaction('\U00002b55')
                    await m.add_reaction('\U0000274c')

                    def react_check(r, u):
                        return u==ctx.author and r.message.channel == ctx.channel


                    r, _u = await self.bot.wait_for('reaction_add', check=react_check)

                    if str(r.emoji) == "\U0000274c":
                        continue
                    else:
                        break

                e = Embed(
                    description = paneru,
                    colour=Colour.from_rgb(133, 208, 243)
                )
                if desc.content == "キャンセル":
                    e.set_author(name=title.content)
                else:
                    e.set_author(name=f'{title.content} | {desc.content}')
                
                await ctx.send('パネルを作成するチャンネルを選択してね')

                channel = await self.dget.text_channel(ctx)

                if channel is None:
                    e = embed.error('チャンネルが見つからなかったよ')
                    return await ctx.send(embed=e)

                mes = await channel.send(embed=e)
                e.set_footer(text=f"パネルID: {mes.id}")
                await mes.edit(embed=e)

                for content in paneru.splitlines():
                    role = re.search(r'(?P<id>[0-9]{18})', content)
                    emoji = content.replace(f'<@&{role.group("id")}>', '').replace(' ', '')
                    await mes.add_reaction(emoji)
                    await self.reaction_role.insert(server=ctx.guild.id, paneru_id=mes.id, title=title.content, channel=channel.id, emoji=emoji, role=int(role.group('id')))

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["reactionrole"])

            elif emoji == 2:
                await ctx.send('編集するパネルのタイトルを入力してね')

                title = await self.bot.wait_for('message', check=check)

                if not (data := await self.reaction_role.fetch(server=ctx.guild.id, title=title.content)):
                    e = embed.error('指定されたタイトルのパネルは見つかりませんでした。')
                    return await ctx.send(embed=e)

                # データのchannelからBOTにキャッシュされてるチャンネルを取得する
                channel = self.bot.get_channel(data['channel'])

                # embedのauthorにタイトルに入ってるものと、そのembedを取得
                e, paneru_embed = await self.get_paneru(channel, title.content)

                # before_descに編集する前のdescriptionを代入
                before_desc = e.description

                await ctx.send("追加する役職と絵文字を\n絵文字A: @AAAA\n絵文字B: @BBBB\nという形で入力してね。\n入力した文章がそのままパネルに表示されるよ。")

                paneru_ = await self.bot.wait_for('message', check=check)

                paneru = paneru_.content

                # 新しいdescriptionを追加
                new_desc = f"{before_desc}\n{paneru}"

                # embedにnew_descとカラーを追加
                ne = Embed(
                    description=new_desc,
                    colour=Colour.from_rgb(133, 208, 243)
                )

                # 新しいembedにauthorとfooterを挿入
                ne.set_author(name=e.author.name)
                ne.set_footer(text=e.footer.text)

                # パネルを新しいembedに変更
                await paneru_embed.edit(embed=ne)

                for content in paneru.splitlines():
                    role = re.search(r'(?P<id>[0-9]{18})', content)
                    emoji = content.replace(f'<@&{role.group("id")}>', '').replace(' ', '')
                    await mes.add_reaction(emoji)
                    await self.reaction_role.insert(server=ctx.guild.id, paneru_id=mes.id, title=title.content, channel=channel.id, emoji=emoji, role=int(role.group('id')))

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["reactionrole"])

            elif emoji == 3:
                role = await self.dget.role(ctx)

                if role is None:
                    e = embed.error('役職は見つからなかったよ')
                    return await ctx.send(embed=e)

                await ctx.send('編集するパネルのタイトルを入力してね')

                title = await self.bot.wait_for('message', check=check)

                # 入力されたタイトルとサーバーIDからデータを取得する
                if not (data := await self.reaction_role.fetch(server=ctx.guild.id, title=title.content, role=role.id)):
                    e = embed.error('指定されたタイトルのパネルは見つかりませんでした。')
                    return await ctx.send(embed=e)

                # データのchannelからBOTにキャッシュされてるチャンネルを取得する
                channel = self.bot.get_channel(data['channel'])

                # embedのauthorにタイトルに入ってるものと、そのembedを取得
                e, paneru = await self.get_paneru(channel, title.content)

                # before_descに編集する前のdescriptionを代入
                before_desc = e.description

                new_desc = [line for line in before_desc.splitlines(
                ) if not line.startswith(f':{data["emoji"]}')]

                ne = Embed(
                    description='\n'.join(new_desc),
                    colour=Colour.from_rgb(133, 208, 243)
                )

                # 新しいembedにauthorとfooterを挿入
                ne.set_author(name=e.author.name)
                ne.set_footer(text=e.footer.text)

                # パネルを新しいembedに変更
                await paneru.edit(embed=ne)

                await paneru.remove_reaction(data["emoji"], paneru.author)

                # データを削除
                await self.reaction_role.delete(server=ctx.guild.id,title=title.content, channel=paneru.channel.id, emoji=data['emoji'])

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["reactionrole"])

            elif emoji == 4:
                await ctx.send('削除するパネルのタイトルを入力してね')
                title = await self.bot.wait_for('message', check=check)

                # 入力されたタイトルとサーバーIDからデータを取得する
                if not (data := await self.reaction_role.fetch(server=ctx.guild.id, title=title.content)):
                    e = embed.error('指定されたタイトルのパネルは見つかりませんでした。')
                    return await ctx.send(embed=e)

                # データのchannelからBOTにキャッシュされてるチャンネルを取得する
                channel = self.bot.get_channel(data['channel'])

                # embedのauthorにタイトルに入ってるものと、そのembedを取得
                _e, paneru = await self.get_paneru(channel, title.content)

                # titleの役職と絵文字一覧を取得
                datas = await self.reaction_role.fetchs(server=ctx.guild.id, title=title.content)

                # datasから役職と絵文字を一つずつ取得して、削除
                for data_ in datas:
                    await self.reaction_role.delete(server=ctx.guild.id, title=title.content, channel=data_['channel'], emoji=data_['emoji'], role=data_['role'])

                # パネルメッセージを削除
                await paneru.delete()

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["reactionrole"])

            else:
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                await ctx.send(embed=e)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["reactionrole"])

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
    async def spre(self, ctx):
        "プレフィックスの設定"

        def check(m):
            return ctx.author == m.author and m.channel == ctx.channel

        e = Embed(
            description="1: プレフィックスの追加\n2: プレフィックスの削除\nキャンセル"
        )
        e.set_author(
            name="なんの設定をする？番号を入力してね | 1回のコマンドで複数個設定できるよ。設定が終わったら`キャンセル`と入力してね")
        default_mes = await ctx.send(embed=e)
        load_emoji = self.bot.get_emoji(773858253884227594)
        await default_mes.add_reaction(load_emoji)

        while True:
            check_setting_number = await self.bot.wait_for('message', check=check)
            if check_setting_number.content == 'キャンセル':
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)
                

            elif check_setting_number.content == '1':
                prefixes = await self.prefix.fetch(server=ctx.guild.id)

                if len(prefixes['prefixes']) == 3:
                    if self.plan.check_plan(ctx.guild, ctx.author):
                        return await self.plan.said_paid(ctx)

                await ctx.send('新しいプレフィックスを入力してね')

                prefix = await self.bot.wait_for('message', check=check)

                if prefix.content not in prefixes['prefixes']:
                    await self.prefix.add(prefixes=prefix.content, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

            elif check_setting_number.content == '2':
                prefixes = await self.prefix.fetch(server=ctx.guild.id)

                await ctx.send('削除するプレフィックスを入力してね')

                prefix = await self.bot.wait_for('message', check=check)

                if prefix.content == "sa:":
                    if self.plan.check_plan(ctx.guild, ctx.author):
                        return await self.plan.said_paid(ctx)

                if prefix.content in prefixes['prefixes']:
                    await self.prefix.remove(prefixes=prefix.content, server=ctx.guild.id)

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

            else:
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)

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

    @c.command()
    async def stat(self, ctx):
        "カウンターの設定"

        def check(m):
            return ctx.author == m.author and m.channel == ctx.channel

        data = await self.load()

        default_mes, load_emoji = await embed.select(ctx, data["stat"])


        while True:
            emoji = await self.dget.emoji_number(ctx, default_mes)

            if emoji is None:
                continue
         

            if emoji == 6:
               
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)
                

            elif emoji == 1:
                channel = await self.dget.voice_channel(ctx)

                if channel is None:
                    e = embed.error('ボイスチャンネルが見つからなかったよ')
                    return await ctx.send(embed=e)

                if not await self.stats.fetch(server=ctx.guild.id, channel=channel.id):
                    await self.stats.insert(server=ctx.guild.id, channel=channel.id, opt='members')

                else:
                    await self.stats.update(channel=channel.id, server=ctx.guild.id, opt="members")

                await ctx.send('カウンターチャンネルの名前を設定します。名前を入力してね')

                n = await self.bot.wait_for('message', check=check)

                await channel.edit(name=f"{n.content}: {len(ctx.guild.members)}")


                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["stat"])

            elif emoji == 2:
                channel = await self.dget.voice_channel(ctx)

                if channel is None:
                    e = embed.error('ボイスチャンネルが見つからなかったよ')
                    return await ctx.send(embed=e)

                if not await self.stats.fetch(server=ctx.guild.id):
                    await self.stats.insert(server=ctx.guild.id, vc=channel.id)

                else:
                    await self.stats.update(vc=channel.id, server=ctx.guild.id)

                await ctx.send('カウンターチャンネルの名前を設定します。名前を入力してね')

                n = await self.bot.wait_for('message', check=check)

                counter = 0
                for channel in ctx.guild.voice_channels:
                    counter += len(channel.members)

                await channel.edit(name=f"{n.content}: {counter}")


                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["stat"])

            elif emoji == 3:
                channel = await self.dget.voice_channel(ctx)

                if channel is None:
                    e = embed.error('ボイスチャンネルが見つからなかったよ')
                    return await ctx.send(embed=e)

                if not await self.stats.fetch(server=ctx.guild.id, channel=channel.id):
                    await self.stats.insert(server=ctx.guild.id, channel=channel.id, opt='roles')

                await ctx.send('カウンターチャンネルの名前を設定します。名前を入力してね')

                n = await self.bot.wait_for('message', check=check)

                await channel.edit(name=f"{n.content}: {len(ctx.guild.roles)}")


                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["stat"])

            elif emoji == 4:
                channel = await self.dget.voice_channel(ctx)

                if channel is None:
                    e = embed.error('ボイスチャンネルが見つからなかったよ')
                    return await ctx.send(embed=e)

                if not await self.stats.fetch(server=ctx.guild.id, channel=channel.id):
                    await self.stats.insert(server=ctx.guild.id, channel=channel.id, opt='channels')

                await ctx.send('カウンターチャンネルの名前を設定します。名前を入力してね')

                n = await self.bot.wait_for('message', check=check)

                await channel.edit(name=f"{n.content}: {len(ctx.guild.channels)}")


                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["stat"])

            elif emoji == 5:
                channel = await self.dget.voice_channel(ctx)

                if channel is None:
                    e = embed.error('ボイスチャンネルが見つからなかったよ')
                    return await ctx.send(embed=e)

                role = await self.dget.role(ctx)

                if role is None:
                    e = embed.error('役職が見つからなかったよ')
                    return await ctx.send(embed=e)

                if not await self.stats.fetch(server=ctx.guild.id, channel=channel.id):
                    await self.stats.insert(server=ctx.guild.id, channel=channel.id, role=role.id)

                else:
                    await self.stats.update(channel=channel.id, server=ctx.guild.id, role=role.id)
                    await self.stats.update(role=role.id, server=ctx.guild.id, channel=channel.id)

                await ctx.send('カウンターチャンネルの名前を設定します。名前を入力してね')

                n = await self.bot.wait_for('message', check=check)

                await channel.edit(name=f"{n.content}: {len(role.members)}")

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["stat"])

            else:
               
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)

    @c.command()
    async def usertime(self, ctx):
        "ブラックリスト・ホワイトチャンネルの設定"
        def check(m):
            return ctx.author == m.author and m.channel == ctx.channel

        if not await self.bc.fetch(server=ctx.guild.id):
            await self.bc.insert(server=ctx.guild.id)

        if not await self.wc.fetch(server=ctx.guild.id):
            await self.wc.insert(server=ctx.guild.id)

        data = await self.load()

        default_mes, load_emoji = await embed.select(ctx, data["usertime"])


        while True:
            emoji = await self.dget.emoji_number(ctx, default_mes)

            if emoji is None:
                continue

            if emoji == 5:
                
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)
                

            elif emoji == 6:
                e = Embed(
                    description="1: ボイスチャンネル\n2: カテゴリーチャンネル\nキャンセル"
                )
                e.set_footer(text="どっちで設定するか番号を入力してね")
                await ctx.send(embed=e)

                n = await self.bot.wait_for('message', check=check)

                if n.content == '1':
                    channel = await self.dget.voice_channel(ctx)

                    if channel is None:
                        e = embed.error('チャンネルが見つからなかったよ')
                        return await ctx.send(embed=e)

                else:
                    channel = await self.dget.category_channel(ctx)

                    if channel is None:
                        e = embed.error('チャンネルが見つからなかったよ')
                        return await ctx.send(embed=e)

                await self.bc.add(channels=channel.id, server=ctx.guild.id)

           

                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)
                default_mes, load_emoji = await embed.select(ctx, data["usertime"])

            elif emoji == 2:
                e = Embed(
                    description="1: ボイスチャンネル\n2: カテゴリーチャンネル\nキャンセル"
                )
                e.set_footer(text="どっちで設定するか番号を入力してね")
                await ctx.send(embed=e)

                n = await self.bot.wait_for('message', check=check)

                if n.content == '1':
                    channel = await self.dget.voice_channel(ctx)

                    if channel is None:
                        e = embed.error('チャンネルが見つからなかったよ')
                        return await ctx.send(embed=e)

                else:
                    channel = await self.dget.category_channel(ctx)

                    if channel is None:
                        e = embed.error('チャンネルが見つからなかったよ')
                        return await ctx.send(embed=e)

                await self.bc.remove(channels=channel.id, server=ctx.guild.id)


                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)
                default_mes, load_emoji = await embed.select(ctx, data["usertime"])

            elif emoji == 3:
                e = Embed(
                    description="1: ボイスチャンネル\n2: カテゴリーチャンネル\nキャンセル"
                )
                e.set_footer(text="どっちで設定するか番号を入力してね")
                await ctx.send(embed=e)

                n = await self.bot.wait_for('message', check=check)

                if n.content == '1':
                    channel = await self.dget.voice_channel(ctx)

                    if channel is None:
                        e = embed.error('チャンネルが見つからなかったよ')
                        return await ctx.send(embed=e)

                else:
                    channel = await self.dget.category_channel(ctx)

                    if channel is None:
                        e = embed.error('チャンネルが見つからなかったよ')
                        return await ctx.send(embed=e)

                await self.wc.add(channels=channel.id, server=ctx.guild.id)


                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)
                default_mes, load_emoji = await embed.select(ctx, data["usertime"])

            elif emoji == 4:
                e = Embed(
                    description="1: ボイスチャンネル\n2: カテゴリーチャンネル\nキャンセル"
                )
                e.set_footer(text="どっちで設定するか番号を入力してね")
                await ctx.send(embed=e)

                n = await self.bot.wait_for('message', check=check)

                if n.content == '1':
                    channel = await self.dget.voice_channel(ctx)

                    if channel is None:
                        e = embed.error('チャンネルが見つからなかったよ')
                        return await ctx.send(embed=e)

                else:
                    channel = await self.dget.category_channel(ctx)

                    if channel is None:
                        e = embed.error('チャンネルが見つからなかったよ')
                        return await ctx.send(embed=e)

                await self.wc.remove(channels=channel.id, server=ctx.guild.id)


                e = embed.succes(desc="保存に成功したよ。次の番号又はキャンセルと入力してね")
                await ctx.send(embed=e)

                default_mes, load_emoji = await embed.select(ctx, data["usertime"])

            else:
                await default_mes.remove_reaction(load_emoji, self.bot.user)
                e = embed.succes(desc="処理が正常に終了したよ")
                return await ctx.send(embed=e)


    @c.command()
    async def stv(self, ctx):
        "コマンドが送信されたTCとVCを紐付ける"

        e = Embed(
            title="詳しくはこのサイトをご覧ください",
            url="https://qiita.com/furimu/items/271895e3206e909a2a77#2-%E8%87%AA%E5%8B%95%E5%85%A5%E9%80%80%E5%87%BA%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6",
            colour=Colour.from_rgb(133, 208, 243)
        )
        await ctx.send(embed=e)

        if ctx.author.voice is None:
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            def voice_check(member, before, after):
                return member==ctx.author
            

            e = Embed(
                title = "下記の中のどれかを`実行`して、このTCと紐付けるVCを接続してね",
                description = "・チャンネル名を入力する\n・コマンド送信者が紐付けるVCに入る",
                colour=Colour.from_rgb(133, 208, 243)
            )

            mw = await ctx.send(embed=e)


            wait_voice = create_task(self.bot.wait_for('voice_state_update', check=voice_check), name="wait_voice")
            wait_number = create_task(self.bot.wait_for('message', check=check), name="wait_number")
            

            aws = {wait_number, wait_voice}

            done, _pending = await wait(aws, return_when=FIRST_COMPLETED)

            task_type = list(done)[0].get_name()

            if task_type=="wait_voice":
                voice = ctx.author.voice.channel
                await mw.delete()

            elif task_type == "wait_number":
                channels = [channel for channel in ctx.guild.voice_channels if wait_number.result().content in channel.name]

                if channels == []:
                    e = embed.error('チャンネルが見つからなかったよ')
                    return await ctx.send(embed=e)

                if len(channels) == 1:
                    voice = channels[0]

                else:
                    channels_number = [f"{i}: {channel.mention}" for i, channel in enumerate(channels, 1)]

                    channels_ = "\n".join(channels_number)
                    await ctx.send(f"{channels_}\n上記から番号を入力してね")

                    get_number = await self.bot.wait_for('message', check=check)

                    try:
                        number = int(get_number.content) - 1
                    except ValueError:
                        return None

                    voice = channels[number]

        else:
            voice = ctx.author.voice.channel

        if not await self.tv.fetch(server=ctx.guild.id, tc=ctx.channel.id):
            await self.tv.insert(server=ctx.guild.id, tc=ctx.channel.id, vc=voice.id)

        else:
            await self.tv.update(vc=voice.id)

        e = Embed(
            description=f"VC: {voice.name}\nTC: {ctx.channel.mention}\n上記の通り紐づけたよ"
        )
        await ctx.send(embed=e)


    @c.command()
    async def srl(self, ctx):
        voice = ctx.author.voice

        if voice is None:

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            def voice_check(member, before, after):
                return member==ctx.author


            messages = []
            for i in range(0, len(ctx.guild.voice_channels), 30):
                channels = "\n".join(f"{number}: {f'`{channel.category.name}` - ' if channel.category else ''}{channel.mention}" for number,
                                    channel in enumerate(ctx.guild.voice_channels[i:i+30], i + 1))
                e = Embed(
                    description=channels
                )
                e.set_author(name="番号を入力してね")
                w = await ctx.send(embed=e)
                messages.append(w.id)

            e = Embed(
                title = "下記の中のどれかを`実行`して、このTCと紐付けるVCを接続してね",
                description = "・上記の中からチャンネルの番号を入力\n・直接チャンネル名かIDを入力\n・コマンド送信者が紐付けるVCに入る",
                colour=Colour.from_rgb(133, 208, 243)
            )

            mw = await ctx.send(embed=e)


            wait_voice = create_task(self.bot.wait_for('voice_state_update', check=voice_check), name="wait_voice")
            wait_number = create_task(self.bot.wait_for('message', check=check), name="wait_number")
            

            aws = {wait_number, wait_voice}

            done, _pending = await wait(aws, return_when=FIRST_COMPLETED)

            task_type = list(done)[0].get_name()

            if task_type == "wait_voice":
                voice = ctx.author.voice.channel

            elif task_type == "wait_number":
                voice = self.dget.get_voice_channel(ctx, wait_number.result().content)

                if voice is None:
                    e = embed.error('VCが見つからなかったよ。はじめからやり直してね')
                    return await ctx.send(embed=e)

                for mes in messages:
                    m = await ctx.channel.fetch_message(mes)
                    await m.delete()
                
                await mw.delete()

        else:
            voice = ctx.author.voice.channel

        if not await self.real_time.fetch(server=ctx.guild.id, tc=ctx.channel.id):
            await self.real_time.insert(server=ctx.guild.id, tc=ctx.channel.id)

        await self.real_time.update(vc=voice.id, server=ctx.guild.id, tc=ctx.channel.id)

        e = Embed(
            description = f"TC: {ctx.channel.mention}\nVC: {voice.name}\n上記の通り紐づけたよ"
        )

        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Setting(bot))
