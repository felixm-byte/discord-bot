from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)

if not os.getenv('DISCORD_TOKEN' or len(os.getenv('DISCORD_TOKEN')) != 59):
    DISCORD_TOKEN = input("Please enter the Discord token:")
    print("Please enter the Google token:")
    GOOGLE_TOKEN = input()
    print("Please enter the Google hyperspecific token:")
    GOOGLE_HYPERSPECIFIC_TOKEN = input()
    print("Please enter the Google specific token:")
    GOOGLE_SPECIFIC_TOKEN = input()
    print("Please enter the Google general token:")
    GOOGLE_GENERAL_TOKEN = input()

    with open('.env', 'w') as f:
        f.write(f"DISCORD_TOKEN={DISCORD_TOKEN}\n")
        f.write(f"GOOGLE_TOKEN={GOOGLE_TOKEN}\n")
        f.write(f"GOOGLE_HYPERSPECIFIC_TOKEN={GOOGLE_HYPERSPECIFIC_TOKEN}\n")
        f.write(f"GOOGLE_SPECIFIC_TOKEN={GOOGLE_SPECIFIC_TOKEN}\n")
        f.write(f"GOOGLE_GENERAL_TOKEN={GOOGLE_GENERAL_TOKEN}\n")
else:
    print("Using existing .env file.")
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    GOOGLE_TOKEN = os.getenv('GOOGLE_TOKEN')
    GOOGLE_HYPERSPECIFIC_TOKEN = os.getenv('GOOGLE_HYPERSPECIFIC_TOKEN')
    GOOGLE_SPECIFIC_TOKEN = os.getenv('GOOGLE_SPECIFIC_TOKEN')
    GOOGLE_GENERAL_TOKEN = os.getenv('GOOGLE_GENERAL_TOKEN')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.hybrid_command()
async def search(ctx, arg):
    try:
        arg = arg.lower()
        res = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_TOKEN}&cx={GOOGLE_HYPERSPECIFIC_TOKEN}={arg}")
        print(res.text)
        res = res.json()
        if not ('items' in res.keys()) or res["items"] == []:
            res = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_TOKEN}&cx={GOOGLE_SPECIFIC_TOKEN}&q={arg}")
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
        res = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_TOKEN}&cx={GOOGLE_GENERAL_TOKEN}&q={arg}")
        print(res.text)
        res = res.json()
        if not ('items' in res.keys()) or res["items"] == []:
            await ctx.send(f"No results found for {arg}, please try again with a different search term.")
        else:
            await ctx.send(f"Result: {res["items"][0]["title"]} \nFrom: {res["items"][0]["displayLink"]} \nLink: {res["items"][0]["link"]}")
    except Exception as e:
        await ctx.send(f"An unexpected error occured. Try using a different search query, or share this code with an admin if that doesn't work: \n{e}")

client.run(DISCORD_TOKEN)
