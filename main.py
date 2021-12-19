import discord
import json
import os
import datetime
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
client = commands.Bot(command_prefix = "?", activity=discord.Game("I'm online done"), intents = discord.Intents.all())

@tasks.loop(seconds=3600)
async def firstloop():
    current = int(datetime.datetime.now().strftime("%H"))
    channel = client.get_channel(832245157889441855)
    if current == 7:
        await channel.send("Half a minute")
    else:
        pass

firstloop.start()

@client.event
async def on_ready():
    print('Bot is ready!')

@client.command()
async def ping(ctx):
    await ctx.send(f"Current ms: `{round(client.latency * 100)}`")


@client.command()
async def changestatus(ctx, arg, *, text):
    if arg == 'watch':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
    elif arg == 'listen':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))
    elif arg == 'play':
        await client.change_presence(activity=discord.Game(name=text))
    elif arg == 'compet':
        await client.change_presence(activity = discord.Activity(type=discord.ActivityType.competing, name=text))

    await ctx.send(f"Changed the bot presence status as {text}!")
botToken = os.environ.get("botToken")
client.run(botToken)