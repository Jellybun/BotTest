import discord
import json
import os
import datetime
import asyncio
from discord.ext import commands, tasks

client = commands.Bot(command_prefix = "?", activity=discord.Game("Doma"), intents = discord.Intents.all())

@tasks.loop(hours=24)
async def firstloop():
    current = int(datetime.datetime.now().strftime("%H"))
    channel = client.get_channel(832245157889441855)
    jelly = client.get_user(759756236996083713)
    if current == 8:
        await channel.send(f"{jelly.mention}\nResetting the status")
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
    elif arg == 'stream':
        await ctx.send("Enter the url of your stream:")
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        try:
            message = await client.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Cooldown is up!")
        else:
            await ctx.send(f"Url: {message}")
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=text, url=message)) 
    await ctx.send(f"Changed the bot presence status as {text}!")

TOKEN = os.getenv("TOKEN")
client.run(TOKEN)