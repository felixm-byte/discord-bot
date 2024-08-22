import os 

import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)

DISCORD_TOKEN = "" 
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.hybrid_command()
async def search(ctx, arg):
    arg = arg.lower()
    res = requests.get(f"https://www.googleapis.com/customsearch/v1?key=&cx=a48e7f7f7b07c44ca&q={arg}")
    print(res.text)
    res = res.json()
    await ctx.send(f"Result: {res["items"][0]["title"]} \nFrom: {res["items"][0]["displayLink"]} \nLink: {res["items"][0]["link"]}")

client.run(DISCORD_TOKEN)