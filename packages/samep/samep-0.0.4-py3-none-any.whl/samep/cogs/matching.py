from discord.ext import commands as c
from discord import Embed, Colour, TextChannel, Role, PermissionOverwrite, utils, errors, Colour
from asyncio import TimeoutError
from datetime import datetime, timedelta
from asyncpgw import general

#pylint: disable=import-error
from samep.cogs.utils import embed

baserole_table = """base_role(
    server bigint,
    base_boy_role bigint,
    base_girl_role bigint
)"""

matching_table = """base_matching(
    server bigint,
    paneru_mes bigint,
    
    boy_role bigint,
    girl_role bigint,
    boy_channel bigint,
    girl_channel bigint,
    template text,
    post_emoji text,
    edit_emoji text,
    del_emoji text
)"""

matchi_table_ = """matchi(
    paneru_mes bigint,
    member bigint,
    channel bigint,
    mes bigint
)

"""

"""
baseboyrole 男性についてる役職(メンションなし)
boyrole 男性についてる役職(メンションあり)
boychannel 男性の投稿文を送信するチャンネル
baseboyrole 男性についてる役職(メンションなし)
girlrole 女性についてる役職(メンションあり)
girlchannel 女性の投稿文を送信するチャンネル
"""


class Matching(c.Cog, name="マッチングテスト", command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.base_matching = general.Pg(bot, 'base_matching')
        self.base_role_ = general.Pg(bot, 'base_role')
        self.matching = general.Pg(bot, 'matchi')


    async def get_new_channel(self, payload, guild, data):
        """募集分を記入するチャンネルを作成
        
        params:
            payload: payload,
            guild: リアクションを押したチャンネル,
            data: matchingテーブルから取得したデータ
        """

        
        channel = self.bot.get_channel(payload.channel_id)

        overwrites = {
            guild.default_role: PermissionOverwrite(read_messages=False),
            guild.me: PermissionOverwrite(read_messages=True),
            payload.member: PermissionOverwrite(read_messages=True)
        }

        "ユーザーの名前のチャンネルが合ったらそれを使う、無かったら削除"
        if any(c.name == payload.member.display_name for c in channel.category.text_channels):
            new_channel = utils.get(channel.category.text_channels, name=payload.member.display_name)

        else:
           new_channel=await channel.category.create_text_channel(name=payload.member.display_name, overwrites=overwrites, position=0) 

        #base_matchingからデータを取得
        temp = await self.base_matching.fetch(paneru_mes=payload.message_id, post_emoji=str(payload.emoji))
        if temp is not None:
            await new_channel.send(f"{payload.member.mention}\n{data['post_emoji']}こちらは代理投稿用の記入画面です。\n下記のテンプレートを使用し、募集文を投稿してください。\n:warning:このチャンネルは５分後自動的に消滅します。\n`キャンセル`と入力すると、投稿せずにこのチャンネルを削除します。\n\n　 　↓　↓ テンプレート ↓　↓")
            await new_channel.send(temp['template'])
            return new_channel

        else:
            temp = await self.base_matching.fetch(paneru_mes=payload.message_id, edit_emoji=str(payload.emoji))
            await new_channel.send(f"{payload.member.mention}\n{data['edit_emoji']}こちらは代理編集用の記入画面です。\n下記のテンプレートを使用し、募集文を編集してください。\n:warning:このチャンネルは５分後自動的に消滅します。\n`キャンセル`と入力すると、投稿せずにこのチャンネルを削除します。\n\n　 　↓　↓ テンプレート ↓　↓")
            await new_channel.send(temp['template'])
            return new_channel

    
    async def check_anony_react(self, mes, content):
        """募集分に匿名リアクションがついてるか確認
        
        params:
            mes: discord.Message,
            content: 募集文
        """

        if '匿名リアクション' in content:
            await mes.add_reaction('\U0000270b')
            await mes.add_reaction('\U0000274e')

        else:
            await mes.clear_reactions()


    async def check_recruit(self, opt, member, channel, base_data, data):
        """役職と募集分の確認
        
        params:
            opt: オプション send=募集分を既に出してるのに新しく開始しようとしてる,
            member: リアクションを押した張本人,
            channel: リアクションを押したチャンネル,
            base_data: base_matchingテーブル,
            data: matchi
        """


        #通知が行かない役職の湯特
        base_role = await self.base_role_.fetch(server=member.guild.id)
        boy_role = member.guild.get_role(base_role['base_boy_role'])
        girl_role = member.guild.get_role(base_role['base_girl_role'])

        #男性役職を持ってたら、男性投稿文、女性役職を持ってたら女性投稿文
        if boy_role in member.roles:
            c = self.bot.get_channel(base_data['boy_channel'])
        elif girl_role in member.roles:
            c = self.bot.get_channel(base_data['girl_channel'])
   
        try:
            # オプションが送信だったら、募集済みのメッセージを送信　
            if opt == "send":
                await c.fetch_message(data['mes'])
                e = embed.error(f'既に{str(c)}で募集をしています。募集を新たにしたい場合は、{channel.mention}の:wastebasket:を押して、前回の募集を削除してください。')
                return await member.send(embed=e)

            #それ以外なら投稿文が見つからなかったのを取得
            else:
                e = embed.error(f'【{str(c)}】にあなたの投稿文は見つかりませんでした。')
            await member.send(embed=e)
        #管理者が消した場合の対応
        except errors.NotFound:
            user_datas = await self.matching.fetchs(member=member.id)
            for user_data in user_datas:
                await self.matching.delete(mes=user_data['mes'], member=member.id)

            e = Embed(
                title = str(member),
                description = "データの消去をしました"
            )
            e.set_footer(text=f"《削除日時》{datetime.now().strftime('%m月%d日%H時%M分')}\n{channel.guild.name}")
            #なにか言われたときのためにログを送信
            await self.bot.get_channel(772406361819971604).send(embed=e)

            
            



    async def check_role(self, payload, member, guild, emoji, base_data):
        """リアクションを押したユーザーの役職の確認
        
        params:
            payload: payload,
            member: リアクションを押した張本人,
            guild: リアクションを押したサーバー,
            emoji: 押されたリアクション,
            base_data: base_matching

        return role[メンションをする役職], requchannel[投稿文を送信するチャンネル], colour[embedの色]
        """

        #パネルのデータを取得、送信無かったら、編集を繰り返す
        paneru_data = await self.base_matching.fetch(paneru_mes=payload.message_id, post_emoji=str(payload.emoji))
        if paneru_data is None:
            paneru_data = await self.base_matching.fetch(paneru_mes=payload.message_id, edit_emoji=str(payload.emoji))
            if paneru_data is None:
                paneru_data = await self.base_matching.fetch(paneru_mes=payload.message_id, del_emoji=str(payload.emoji))


        #通知が行かない役職の取得
        base_role = await self.base_role_.fetch(server=member.guild.id)

        boy_role = guild.get_role(base_role['base_boy_role'])
        girl_role= guild.get_role(base_role['base_girl_role'])

        #役職を両方付けてた時の対処
        if boy_role in member.roles and girl_role in member.roles:
            e = embed.error(f'貴方には{str(boy_role)}・{str(girl_role)}２つの役職がついてつため、募集をすることが出来ません。')
            await member.send(embed=e)

            role = None
            requchannel = None
            colour= None

        

        elif boy_role in member.roles:
            role = guild.get_role(base_data['girl_role'])
            requchannel = self.bot.get_channel(base_data['boy_channel'])
            colour = Colour.blue()

        elif girl_role in member.roles:
            role = guild.get_role(base_data['boy_role'])
            requchannel = self.bot.get_channel(base_data['girl_channel'])
            colour = Colour.red()

        else:
            e = embed.error(f'貴方には{str(boy_role)}・{str(girl_role)}どちらかの役職が付いて居ないため募集をすることが出来ません。')
            await member.send(embed=e)

            role = None
            requchannel = None
            colour = None

        return role, requchannel, colour


    async def send_embed(self, payload, m, emoji, base_data):
        """募集分の投稿
        
        params:
            payload: payload,
            m: discord.Message,
            emoji: 押されたリアクション,
            base_data: base_matching

        return requ_mes[投稿した募集文]
        """

        role, target, colour = await self.check_role(payload, m.author, m.guild, emoji, base_data)

        if role is None:
            requmes = None
            return requmes

        e = Embed(
            description = m.content,
            colour = colour
        )
        e.set_author(name=m.author.display_name, icon_url=m.author.avatar_url)
        e.set_thumbnail(url=m.author.avatar_url)
        e.set_footer(text=f"{str(m.author)} | {m.author.id}")
        requ_mes = await target.send(role.mention, embed=e)
        await self.check_anony_react(requ_mes, m.content)
        return requ_mes

    
    async def edit_embed(self, payload, m, content, emoji, base_data, data):
        """募集分の編集

        params:
            payload: payload,
            m: discord.Message,
            emoji: 押されたリアクション,
            base_data: base_matching
        
        return requ_mes[編集した募集文]
        """
        role, target, colour = await self.check_role(payload, m, m.guild, emoji, base_data)
        
        mes = await target.fetch_message(data['mes'])

        if role is None:
            requmes = None
            return requmes

        e = Embed(
            description = content,
            colour = colour
        )
        e.set_author(name=m.display_name, icon_url=m.avatar_url)
        e.set_thumbnail(url=m.avatar_url)
        e.set_footer(text=f"{str(m)} | {m.id}")
        requ_mes = await mes.edit(content=role.mention, embed=e)
        await self.check_anony_react(mes, content)
        return requ_mes


    async def send_poster(self, payload, requmes, base_data):
        """投稿が完了した時のお知らせ
        
        params:
            payload: payload,
            requmes: discord.Message 募集文,
            base_data: base_matching

        return e_m[お知らせ]
        """
        mm = self.bot.get_channel(payload.channel_id)
        _role, _channel, colour = await self.check_role(payload, payload.member, mm.guild, payload.emoji, base_data)
        e = Embed(
            title = f"{base_data['post_emoji']} 代理投稿完了 {base_data['post_emoji']}",
            description = f"{requmes.content}\n編集削除は{mm.mention}の{base_data['edit_emoji']}{base_data['del_emoji']}ボタンを押してください。",
            colour = colour
        )

        e.set_footer(text=f"《投稿日時》{datetime.now().strftime('%m月%d日%H時%M分')}\n{mm.guild.name} / {mm.name}")

        e_m = await payload.member.send(embed=e)

        return e_m

    
    async def send_editer(self, payload, requmes, base_data):
        """編集が完了した時のお知らせ
        
        params:
            payload: payload,
            requmes: discord.Message 募集文,
            base_data: base_matching

        return e_m[お知らせ]
        """
        mm = self.bot.get_channel(payload.channel_id)
        _role, channel, colour = await self.check_role(payload, payload.member, mm.guild, payload.emoji, base_data)
        
        e = Embed(
            title = f"{base_data['edit_emoji']} 編集処理完了 {base_data['edit_emoji']}",
            description = f"{requmes.content}\n編集削除は{mm.mention}の{base_data['edit_emoji']}{base_data['del_emoji']}ボタンを押してください。",
            colour = colour
        )

        e.set_footer(text=f"《投稿日時》{datetime.now().strftime('%m月%d日%H時%M分')}\n{channel.guild.name} / {channel.name}")

        e_m = await payload.member.send(embed=e)

        return e_m


    async def send_deleter(self, payload, base_data):
        """削除が完了した時のお知らせ
        
        params:
            payload: payload,
            requmes: discord.Message 募集文,
            base_data: base_matching

        return e_m[お知らせ]
        """
        guild = self.bot.get_guild(payload.guild_id)
        _role, channel, colour = await self.check_role(payload, payload.member, guild, payload.emoji, base_data)
        e = Embed(
            title = f"{base_data['del_emoji']} 削除処理完了 {base_data['del_emoji']}",
            colour = colour
        )

        e.set_footer(text=f"《投稿日時》{datetime.now().strftime('%m月%d日%H時%M分')}\n{channel.guild.name} / {channel.name}")

        e_m = await payload.member.send(embed=e)

        return e_m




    @c.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id is None:
            return
        if payload.member.bot:
            return


        guild = self.bot.get_guild(payload.guild_id)
        channel = self.bot.get_channel(payload.channel_id)
        #メッセージが見つからなかったら戻る
        try:
            mes = await channel.fetch_message(payload.message_id)
            mes_create_time = mes.created_at + timedelta(hours=9)
        except errors.HTTPException:
            return

        #リアクションが押されたembedにリアクションを押したユーザーのIDが合ったら、立候補のお知らせ
        if str(payload.emoji) == '\U0000270b':
            
            if not (embeds := mes.embeds):
                return

            if not (data := await self.matching.fetch(mes=mes.id)):
                return

            await mes.remove_reaction(payload.emoji, payload.member)

            member = guild.get_member(data['member'])

            for e in embeds:
                if str(member.id) not in e.footer.text:
                    return

            await member.send(f":person_raising_hand: {payload.member.display_name} から 立候補(匿名)\n【ｱｶｳﾝﾄ名】@{str(payload.member)}\n【投稿日時】{mes_create_time.strftime('%m月%d日 %H時%M分')}\n({guild.name} / #{str(channel)})\n------------------------------------------")

            await payload.member.send(f"✋ {member.display_name} へ 立候補完了\n【ｱｶｳﾝﾄ名】@{str(member)}\n【投稿日時】{mes_create_time.strftime('%m月%d日 %H時%M分')}\n({guild.name} / {channel.mention})\n`取り消しをする場合は、募集文の❎を押してください`\n------------------------------------------")
 

        #取り消し
        elif str(payload.emoji) == '\U0000274e':
            
            if not (embeds := mes.embeds):
                return

            if not (data := await self.matching.fetch(mes=mes.id)):
                return
            await mes.remove_reaction(payload.emoji, payload.member)
            member = guild.get_member(data['member'])

            for e in embeds:
                if str(member.id) not in e.footer.text:
                    return

            await member.send(f":pray: {payload.member.display_name} から 取消\n【アカウント名】@{str(payload.member)}\n【投稿日時】{mes_create_time.strftime('%m月%d日 %H時%M分')}\n({guild.name} / #{str(channel)})\n------------------------------------------")

            await payload.member.send(f"❎ {member.display_name} へ 取消完了 \n【アカウント名】@{str(member)}\n【投稿日時】{mes_create_time.strftime('%m月%d日 %H時%M分')}\n({guild.name} / {channel.mention})\n------------------------------------------")

        

        if not (base_data := await self.base_matching.fetch(paneru_mes=mes.id)):
            return

        #matchingにデータが存在したら戻る
        if str(payload.emoji) == base_data['post_emoji']:
            await mes.remove_reaction(payload.emoji, payload.member)

            if (data := await self.matching.fetch(paneru_mes=mes.id, member=payload.member.id)):
                return await self.check_recruit('send', payload.member, channel, base_data, data)

                
            #募集分を送信するチャンネルを取得
            new_channel = await self.get_new_channel(payload, guild, base_data)

            def check(m):
                return m.author == payload.member and m.channel == new_channel

            try:
                requ = await self.bot.wait_for('message', check=check, timeout=300.0)

                await new_channel.delete()

                if requ.content == "キャンセル":
                    return

            except TimeoutError:
                return await new_channel.delete()

            #役職の確認
            _role, target, _colour = await self.check_role(payload, payload.member, guild, str(payload.emoji), base_data)

            #募集分を送信
            requ_mes= await self.send_embed(payload, requ, str(payload.emoji), base_data)


            #募集分を取得
            sent_mes = await target.fetch_message(requ_mes.id)
            #dbに突っ込む
            await self.matching.insert(paneru_mes=mes.id, member=payload.member.id, channel = target.id, mes=sent_mes.id)
            #募集者に完了のお知らせを送信
            await self.send_poster(payload, requ, base_data)

        elif str(payload.emoji) == base_data['edit_emoji']:
            await mes.remove_reaction(payload.emoji, payload.member)

            #募集されなかったら、送信
            if not (data := await self.matching.fetch(paneru_mes=mes.id, member=payload.member.id)):
                await self.check_recruit('edit', payload.member, channel, base_data, data)


            post_channel = self.bot.get_channel(data['channel'])

            post_mes = await post_channel.fetch_message(data['mes'])

            #募集分を送信するチャンネルを取得
            new_channel = await self.get_new_channel(payload, guild, base_data)

            def check(m):
                return m.author == payload.member and m.channel == new_channel

            try:
                requ = await self.bot.wait_for('message', check=check, timeout=300.0)

                await new_channel.delete()

                if requ.content == "キャンセル":
                    return

            except TimeoutError:
                return await new_channel.delete()


            #役職の確認
            _role, target, _colour = await self.check_role(payload, payload.member, guild, str(payload.emoji), base_data)

            #募集文の変更
            await self.edit_embed(payload, payload.member, requ.content, str(payload.emoji), base_data, data)   

            #編集者にお知らせ
            await self.send_editer(payload, requ, base_data)

        elif str(payload.emoji) == base_data['del_emoji']:
            await mes.remove_reaction(payload.emoji, payload.member)
            if not (data := await self.matching.fetch(paneru_mes=mes.id, member=payload.member.id)):
                return await self.check_recruit('del', payload.member, channel, base_data, data)

            post_channel = self.bot.get_channel(data['channel'])

            post_mes = await post_channel.fetch_message(data['mes'])
            
            #役職の確認
            _role, target, _colour = await self.check_role(payload, payload.member, guild, str(payload.emoji), base_data)

            #募集分の削除
            await post_mes.delete()
            #削除完了のメッセージを送信
            await self.send_deleter(payload, base_data)
            #dbのデータを削除
            await self.matching.delete(paneru_mes=mes.id, member=payload.member.id, channel = target.id, mes=data['mes'])