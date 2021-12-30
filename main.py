import discord
import json
import os
import datetime
import asyncio
import requests
from discord.ext import commands, tasks
userBlackList = []

client = commands.Bot(command_prefix = "?", activity=discord.Game("?help"), intents = discord.Intents.all())

def get_apod():
    response = requests.get("https://api.nasa.gov/planetary/apod?api_key=FHlnYmh56cpv8KVLOdW8k2mCdKhAYT47A6XEKZCG")
    json_data = json.loads(response.text)
    return json_data

@client.command()
async def load(ctx, ext):
  client.load_extension(f"cogs.{ext}")

@client.command()
async def unload(ctx, ext):
  client.unload_extension(f"cogs.{ext}")

for file in os.listdir('./cogs'):
  if file.endswith("py"):
    client.load_extension(f'cogs.{file[:-3]}')

@client.event
async def on_ready():
    print('Bot is ready!')


@client.command()
async def ping(ctx):
    embed = discord.Embed(description=f"Current ms: `{round(client.latency * 100)}`")
    await ctx.send(embed=embed)


@client.command()
async def nasa(ctx):
    data = get_apod()
    image = data["hdurl"]
    title = data['title']
    date = data['date']
    explanation = data['explanation']
    author = data['copyright']
    embed = discord.Embed(title=title, description=str(explanation))
    embed.set_author(name=str(author))
    embed.set_image(url=str(image))
    embed.set_footer(text=str(date))
    await ctx.send(embed = embed)

class Blacklist(commands.CheckFailure):
    pass

@client.check
async def userblacklist(ctx):
    if ctx.author.id in userBlackList:
        raise Blacklist('You are temporarily blacklisted from using this bot.')
        return
    else:
        return True


# On Command Error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, Blacklist):
        await ctx.send(error)


TOKEN = os.getenv("TOKEN")
client.run(TOKEN)