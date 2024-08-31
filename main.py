from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests
import os

load_dotenv()

intents = discord.Intents.all()
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
print(DISCORD_TOKEN)
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def search(ctx, *args):
    arg = " ".join(args[:])
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

@client.command()
async def search_google(ctx, *args):
    arg = " ".join(args[:])
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

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="welcome")
    await channel.send(f'Hi {member}, welcome to the server! The Code for Impact hackathon is taking place from the 28-29th of September, and we hope you have a great time! To be ready for the event, please make sure to check out the #announcements channel for updates, and the #resources channel for helpful information. If you have any questions, feel free to ask in the #help-me channel or send a DM to Felix. Have a great day! :smile:')
    await channel.send(f'Devpost: https://go.codeforimpact.dev/')


@client.command()
async def about(ctx):
    await ctx.send("Hi! I'm the Code for Impact bot, and I'm here to help you with any questions you might have about the hackathon. These are our FAQs: \n - When is this hackathon? \n - 28th-29th September \n - How do I sign up? \n - Sign up at https://go.codeforimpact.dev/ \n - Something else? \n - Have a look on the website (codeforimpact.dev) or ask in #help-me. You can also DM Felix if it's urgent/private.")



@client.command()
async def ask_anything(ctx, *args):
    arg = " ".join(args[:])
    res = requests.post(
        "https://jamsapi.hackclub.dev/openai/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENAI_PROXY')}",
            "Content-Type": "application/json",
        },
        json={
            'model': 'gpt-3.5-turbo',
            "messages": [
                {
                    "role": "system",
                    "content": "You are an assistant for the Code for Impact hackathon, which is an effective altruism-themed hackathon for 13-18 year olds. You are here to help answer any questions that participants may have. Please consider your audience, without coming off as too formal or 'hello fellow kids-ish'. You can also say 'I don't know, ask Felix on discord' if you can't answer a question."
                },
                {
                    "role": "user",
                    "content": arg
                }
            ]
        },
    )
    res = res.json()
    print(res)
    await ctx.send(f"Response: {res['choices'][0]['message']['content']}")
    await ctx.send(f"API credit doesn't grow on trees, please use this command sparingly.")

#@client.command()
#async def help(ctx):
#    await ctx.send("These are the commands you can use: \n - /search <query> \n - /search_google <query> \n - /about \n - /ask_anything <question> (not fully implemented) \n - /help")
client.run(DISCORD_TOKEN)