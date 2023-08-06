from discord import Guild, Member
from asyncpgw import general

#pylint: disable=import-error
from utils import embed

class Plan:
    def __init__(self, bot):
        self.bot = bot
        self.plan = general.Pg(bot, 'matching')


    async def check_plan(self, guild: Guild, member: Member):
        suport_server = self.bot.get_guild(754680802578792498)
        if member in suport_server.members:
            return True

        elif not (server_data := await self.plan.fetch(server=guild.id)):
            return True

        elif server_data['plan'] == 1:
            if not server_data['enable']:
                return True

        elif server_data['plan'] == 3 or server_data['enable']:
            return False

        elif not (user_data := await self.plan.fetch(user_id=member.id)):
            return True

        elif user_data['plan'] == 2:
            if not user_data['enable']:
                return True

        elif user_data['plan'] == 4 or user_data['enable']:
            return False

    
    async def send_paid(self, mes):
        if await self.check_plan(mes.guild, mes.author):
            e = embed.error('現在のプランではこれを実行することは出来ません。プランを別のものに変更してください。')
            return await mes.channel.send(embed=e)