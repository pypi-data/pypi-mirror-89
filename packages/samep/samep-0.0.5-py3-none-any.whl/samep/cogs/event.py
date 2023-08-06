from discord.ext import commands as c
from asyncpgw import general
from discord import Role, Embed, PermissionOverwrite, errors, TextChannel, utils, VoiceChannel
from random import shuffle

import asyncio, emoji
#pylint: disable=import-error
from samep.cogs import setting
from samep.cogs.utils import embed, dget


event_table = """event_table(
    server bigint,
    events bigint[] DEFAULT array[] :: bigint[],
    ncvl bigint[] DEFAULT array[] :: bigint[],
    profiles bigint[] DEFAULT array[] :: bigint[],
    osimen bigint,
    osigirl bigint,
    mention bigint,
    channels bigint[] DEFAULT array[] :: bigint[]
)

"""


class Event(c.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.event = general.Pg(bot, 'event_table')
        self.dget = dget.Dget(bot)
        self.profile_channels = [777488787210108938, 777488824124047380, 594027468185403421, 594027498908418049]


    @c.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        channel = self.bot.get_channel(787247607021436958) or self.bot.get_channel(789473014009430047)
        if after.channel:
            if before.channel == after.channel:
                return
            if after.channel not in channel.category.voice_channels:
                return

            

            for profile_ in self.profile_channels:
                profile = self.bot.get_channel(int(profile_))

                if profile is None:
                    continue

                if not (mes :=  await profile.history(limit=None).get(author__id=member.id)):
                    continue

                gender_roles = [role for role in member.roles if role.name in ["Woman", "Man"]]

                role = ":mens:" if gender_roles[0].name == "Man" else ":womens:"

                e = Embed(
                description=f"{role}({str(member)})[プロフはこちら]({mes.jump_url})"
                )
                
                m = await channel.send(member.mention, embed=e)

                await m.add_reaction(emoji.emojize(f':love_letter:', use_aliases=True))
                await m.add_reaction(emoji.emojize(f':wastebasket:', use_aliases=True))
                return

    @c.command(hidden=True)
    async def prof(self, ctx):
        if not (data := await self.event.fetch(server=ctx.guild.id)):
            return
        
        
        if ctx.channel.id not in data["channels"]:
            if ctx.channel.id not in [789473361163845662, 787247607021436958, 789473014009430047]:
                return
        for profile_ in self.profile_channels:
            profile = self.bot.get_channel(int(profile_))

            if profile is None:
                continue

            if (mes :=  await profile.history(limit=None).get(author__id=ctx.author.id)) is None:
                continue

            gender_roles = [role for role in ctx.author.roles if role.name in ["Woman", "Man"]]

            role = ":mens:" if gender_roles[0].name == "Man" else ":womens:"

            e = Embed(
                description=f"{role}({str(ctx.author)})[プロフはこちら]({mes.jump_url})"
            )
            
            m = await ctx.send(ctx.author.mention, embed=e)

            await m.add_reaction(emoji.emojize(f':love_letter:', use_aliases=True))
            await m.add_reaction(emoji.emojize(f':wastebasket:', use_aliases=True))

            await ctx.message.delete()
            return



        

    @c.command(hidden=True)
    async def avr(self, ctx, role: Role):
        "コマンド送信者が接続してるVCのメンバー全員に役職を付与"
        for member in ctx.author.voice.channel.members:
            if member.bot:
                continue
            await member.add_roles(role)

        e = embed.succes(desc=f"{ctx.author.voice.channel.name}に入ってる{len(ctx.author.voice.channel.members)}人に{role.mention}を付けたよ")

        await ctx.send(embed=e)

    @c.command(hidden=True)
    async def cvm(self, ctx, role: Role):
        vc = ctx.author.voice.channel.members
        r = ctx.guild.get_role(771408518070140949)
        c = 1
        for m in vc:
            if r not in m.roles:
                if role in m.roles:
                    v = await ctx.author.voice.channel.clone()
                    await v.edit(name=f"椅子取り- {c}")
                    await m.move_to(v)
                    c += 1       
        

    @c.command(hidden=True)
    async def cvl(self, ctx, channel: VoiceChannel=None):
        "VCの人数制限を変える"

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
       
        await ctx.send('何人制限に変える？数字のみ入力してね')

        limit = await self.bot.wait_for('message', check=check)


        try:
            limit = int(limit.content)

        except ValueError:
            e = embed.error('数字以外が指定されたので、処理を停止したよ')
            return await ctx.send(embed=e)


        for vc in ctx.channel.category.voice_channels:
            if channel:
                if str(vc.id) == channel.id:
                    continue

            await vc.edit(user_limit=limit)

        e = embed.succes('VCの人数制限を変更したよ')
        await ctx.send(embed=e)


    @c.command(hidden=True)
    async def avrl(self, ctx, role: Role=None):
        "タグがついてる人を確認して、タグがついてる人を人数分けする"

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        man=utils.get(ctx.guild.roles, name="Man")


        if role is None:
            e = embed.error('役職が見つからなかったよ')
            return await ctx.send(embed=e)

        rm = [member for member in ctx.author.voice.channel.members if member.voice.channel if role in member.roles]

        role_members = [member for member in rm if member.voice.channel == ctx.author.voice.channel]

        shuffle(role_members)

        e = Embed(
            description = '\n'.join(f'{i}: {member.display_name}({str(member)})' for i, member in enumerate(role_members, 1))
        )
        e.set_footer(text=f"トータル: {len(role_members)}")

        await ctx.send(embed=e)

        await ctx.send('何人ずつに分ける？')
        limit = await self.bot.wait_for('message', check=check)

        await ctx.send('チーム分けを開始するよ')

        for i in range(0, len(role_members), int(limit.content)):
            e = Embed(
                description = '\n'.join(f'{"♂" if man in vmember.roles else "♀"} {vmember.display_name}({str(vmember)})' for vmember in role_members[i:i+int(limit.content)] )
            )
            await ctx.send(embed=e)


    @c.command(hidden=True)
    async def arm(self, ctx, role: Role):
        members = [member for member in ctx.author.voice.channel.members if not member.bot and role in member.roles]

        for member in members:
            m = await ctx.send(f"{member.mention}({str(member)})")
            await m.add_reaction('👍')

        m = await ctx.send('全員分送信が完了しました。このメッセージは10秒後に自動削除されます')
        await asyncio.sleep(10)
        await m.delete()

    @c.command(hidden=True)
    async def add_event(self, ctx, channels: c.Greedy[TextChannel]=None):
        if channels is None:
            e = embed.error('チャンネルが指定されていないよ')
            return await ctx.send(embed=e)

        for channel in channels:
            if not (data := await self.event.fetch(server=ctx.guild.id)):
                await self.event.insert(server=ctx.guild.id)
                await self.event.add(channels=channel.id, server=ctx.guild.id)

            else:
                if channel.id in data["channels"]:
                    continue

                await self.event.add(channels=channel.id, server=ctx.guild.id)

        e = embed.succes(desc='チャンネルの保存に成功したよ')
        await ctx.send(embed=e)
        
        

    @c.Cog.listener()
    async def on_raw_reaction_add(self, payload):
     
        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return
        if payload.member.bot:
            return

        c = self.bot.get_channel(payload.channel_id)

        if c.id in [789473361163845662, 787247607021436958, 789473014009430047]:
            from datetime import datetime
            start = datetime.now()
            mes = await c.fetch_message(payload.message_id)
            
            try:
                mention_member = mes.mentions[0]
            except:
                return

            anony = emoji.emojize(f':love_letter: {mention_member} へ　匿名告白完了', use_aliases=True)
            anony_of_candidacy = emoji.emojize(f':mailbox_with_mail: {payload.member} から　匿名告白受取', use_aliases=True)

            """becoming_a_candidate = emoji.emojize(f':raised_hand: {mention_member} へ　立候補完了', use_aliases=True)
            receipt_of_candidacy = emoji.emojize(f':person_raising_hand: {payload.member}　から　立候補(匿名)受取', use_aliases=True)
            revocation = emoji.emojize(f':negative_squared_cross_mark: {mention_member} へ取消完了', use_aliases=True)
            revocation_of_candidacy = emoji.emojize(f':pray: {payload.member} から　取消希望受取', use_aliases=True)"""
            if str(payload.emoji) == emoji.emojize(f':love_letter:', use_aliases=True):
                await mes.remove_reaction(payload.emoji, payload.member)

                anony = emoji.emojize(f':love_letter: {mention_member} へ 匿名告白完了', use_aliases=True)
                anony_of_candidacy = emoji.emojize(f':mailbox_with_mail: {payload.member} から 匿名告白受取', use_aliases=True)
                
                try:
                    await payload.member.send(f'{anony}\n【ｱｶｳﾝﾄ名】@{str(mention_member)}\n({guild.name}/{c.category.name})\n------------------------------------------')
                    await mention_member.send(f'{anony_of_candidacy}\n【ｱｶｳﾝﾄ名】@{str(payload.member)}\n({guild.name}/{c.category.name})\n------------------------------------------')
                    print(datetime.now() - start)
                except errors.Forbidden:
                    return

            elif str(payload.emoji) == emoji.emojize(f':wastebasket:', use_aliases=True):
                await mes.remove_reaction(payload.emoji, payload.member)
                if payload.member == mention_member:
                    await mes.delete()
            return

        if not (data := await self.event.fetch(server=payload.member.guild.id)):
            return
        
        if c.id not in data["channels"]:
            return

        mes = await c.fetch_message(payload.message_id)
        try:
            mention_member = mes.mentions[0]
        except:
            return

        if str(payload.emoji) == emoji.emojize(f':love_letter:', use_aliases=True):
            await mes.remove_reaction(payload.emoji, payload.member)

            anony = emoji.emojize(f':love_letter: {mention_member} へ 匿名告白完了', use_aliases=True)
            anony_of_candidacy = emoji.emojize(f':mailbox_with_mail: {payload.member} から 匿名告白受取', use_aliases=True)
            
            try:
                await payload.member.send(f'{anony}\n【ｱｶｳﾝﾄ名】@{str(mention_member)}\n({guild.name}/{c.category.name})\n------------------------------------------')
                await mention_member.send(f'{anony_of_candidacy}\n【ｱｶｳﾝﾄ名】@{str(payload.member)}\n({guild.name}/{c.category.name})\n------------------------------------------')
            except errors.Forbidden:
                return

        elif str(payload.emoji) == emoji.emojize(f':wastebasket:', use_aliases=True):
            await mes.remove_reaction(payload.emoji, payload.member)
            if payload.member == mention_member:
                await mes.delete()
            
        
    @c.command(hidden=True)
    async def vcadd(self, ctx, roles: c.Greedy[Role]=None):
        "役職を指定してボイスチャンネルに入ってる人の中で付けてない人に付けるよ"
        if roles is None:
            e = embed.error('役職が指定されてないよ')
            return await ctx.send(embed=e)

        if len(roles) == 1:

            for role in roles:
                if role == roles[0]:
                    continue
                
                for member in ctx.author.voice.channel.members:
                    if role  not in member.roles:
                        await member.add_roles(role)

        else:
            for member in ctx.author.voice.channel.members:
                if roles[0] in ctx.author.voice.channel.members:
                    if roles[1] not in ctx.author.voice.channel.members:
                        await member.add_roles(roles[1])


    @c.command(hidden=True)
    async def vcy(self, ctx, role: Role=None):
        if role is None:
            e = embed.error('役職が指定されてないよ')
            return await ctx.send(embed=e)

        vcm = [member for member in ctx.author.voice.channel.members if role in member.roles]

        e = Embed(
            description = "\n".join(f"{i}: {member.mention}" for i, member in enumerate(vcm, 1))
        )
        e.set_footer(text=f"{ctx.author.voice.channel.name}にいて、{role.name}が付いてるユーザー一覧")

        await ctx.send(embed=e)


    @c.command(hidden=True)
    async def vcr(self, ctx, roles: c.Greedy[Role]=None, opt=None):
        "役職が付いてない人の一覧を出すよ"
        if not (vc := ctx.author.voice):
            e = embed.error('このコマンドはVCに接続してから実行してね')
            return await ctx.send(embed=e)

        if opt is None:
            members = vc.channel.members
        else:
            members = ctx.guild.members

        if len(roles) >= 3:
            e = embed.error('指定できる役職の数は３個までだよ')
            return await ctx.send(embed=e)

        if len(roles) == 1:
            e = Embed(
                description = "\n".join(f"{i}: {member.mention}" for i, member in enumerate(members, 1) if roles[0] not in member.roles)
            )
            e.set_footer(text=f"2: {roles[0]}が付いてない人の一覧")
            return await ctx.send(embed=e)

        e = Embed(
            description = f"1: {roles[0]}と{roles[1]}が付いてる人の一覧を表示\n2: {roles[0]}が付いてる人の中で{roles[1]}が付いてない人の一覧を表示"
        )

        e.set_author(name="番号を入力してね")
        await ctx.send(embed=e)

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        m = await self.bot.wait_for('message', check=check)

        try:
            number = int(m.content)
        except ValueError:
            e = embed.error('指定された番号はありません')
            return await ctx.send(embed=e)


        if number ==1:

            e = Embed(
                description = "\n".join(f"{i}: {member.mention}" for i, member in enumerate(members, 1) if roles[0] in member.roles and roles[1] in member.roles)
            )
            e.set_footer(text=f"{roles[0]}と{roles[1]}が付いてる人の一覧")
            await ctx.send(embed=e)
            

        elif number == 2:
            e = Embed(
                description = '\n'.join(f"{i}: {member.mention}" for i, member in enumerate(members, 1) if roles[0] in member.roles and roles[1] not in member.roles)
            )
            e.set_footer(text=f"{roles[0]}が付いてる人の中で{roles[1]}が付いてない人の一覧")
            await ctx.send(embed=e)