from discord import Embed, Webhook, AsyncWebhookAdapter, utils, Colour
from random import randint
import aiohttp
async def create_webhook(channel):
    if len(await channel.webhooks()) != 0:
        for webhoo in await channel.webhooks():
            return webhoo.url

    else:
        webhoo = await channel.create_webhook(name = '天の声')
        return webhoo.url

async def get_webhook(channel):
    
    
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(await create_webhook(channel), adapter=AsyncWebhookAdapter(session))
        return webhook.url