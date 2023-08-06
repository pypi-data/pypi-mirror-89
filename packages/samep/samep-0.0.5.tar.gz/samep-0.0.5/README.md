# インストール

```
win:
py -3 -m pip install samep
linux:
python3.8 -m pip install samep
```

# 追加項目

## メインファイル

```py
#main.py

from discord.ext import commands as c
from discord import Intents
from asyncpgw import start

import asyncio

class Main(c.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = '!',
            description = 'this is bot',
            intents = Intents.all()
            )
        
        self.tables = []

    async def ps_connect(self):
        "postgresqlに接続"
        self.pool = await start.connect('postgres://username:password@/dbname')


    async def add_table(self, table):
        """postgtesqlに作成するテーブルを追加する"""
        if table not in self.tables:
            self.tables.append(table)


    async def on_ready(self):
        print('起動しました。')

        self.load_extension('samep.extension')

        for table in self.tables:
            await start.create(self.pool, table)


    async def start(self):
        
        await super().start('bot token')

    
    def main(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.ps_connect())
        loop.run_until_complete(self.start())
        loop.close()


if __name__ == '__main__':
    bot = Main()
    bot.main()