from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_TOKEN = os.getenv('GOOGLE_TOKEN')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.hybrid_command()
async def search(ctx, arg):
    try:
        arg = arg.lower()
        res = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_TOKEN}&cx=a48e7f7f7b07c44ca&q={arg}")
        print(res.text)
        res = res.json()
        if not ('items' in res.keys()) or res["items"] == []:
            res = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_TOKEN}&cx=219860434a93544f2&q={arg}")
            print(res.text)
            res = res.json()
            if res["items"] == []:
                await ctx.send(f"No results found for {arg}, please try again with a different search term.")
            else:
                await ctx.send(f"Result: {res["items"][0]["title"]} \nFrom: {res["items"][0]["displayLink"]} \nLink: {res["items"][0]["link"]}")
        else:
            await ctx.send(f"Result: {res["items"][0]["title"]} \nFrom: {res["items"][0]["displayLink"]} \nLink: {res["items"][0]["link"]}")
    except Exception as e:
        await ctx.send(f"An unexpected error occured. Try using a different search query, or share this code with an admin if that doesn't work: \n{e}")

@client.hybrid_command()
async def search_google(ctx, arg):
    try:
        arg = arg.lower()
        res = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_TOKEN}&cx=a1d0a547b253c4652&q={arg}")
        print(res.text)
        res = res.json()
        if not ('items' in res.keys()) or res["items"] == []:
            await ctx.send(f"No results found for {arg}, please try again with a different search term.")
        else:
            await ctx.send(f"Result: {res["items"][0]["title"]} \nFrom: {res["items"][0]["displayLink"]} \nLink: {res["items"][0]["link"]}")
    except Exception as e:
        await ctx.send(f"An unexpected error occured. Try using a different search query, or share this code with an admin if that doesn't work: \n{e}")

client.run(DISCORD_TOKEN)