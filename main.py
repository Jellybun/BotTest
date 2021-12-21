import discord
import json
import os
import datetime
import asyncio
import requests
from discord.ext import commands, tasks
userBlackList = []

client = commands.Bot(command_prefix = "?", activity=discord.Game("Doma"), intents = discord.Intents.all())

def get_apod():
    response = requests.get("https://api.nasa.gov/planetary/apod?api_key=FHlnYmh56cpv8KVLOdW8k2mCdKhAYT47A6XEKZCG")
    json_data = json.loads(response.text)
    return json_data

def get_weather():
    response = requests.get("api.openweathermap.org/data/2.5/weather?q=London&appid={f58168ca28ded38fd2b1f71376b48f31}")
    json_data = json.loads(response.text)
    return json_data



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

@client.command()
async def weather(ctx):
    data = get_weather()
    await ctx.send(data[1])

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
@client.command()
async def given(ctx):
    role = ctx.guild.get_role(922763949148094515)
    members = role.members
    for i in members:
        await i.send(f"{ctx.message.jump_url} this is a test as well")
@client.command()
async def changestatus(ctx, arg = None, *, text = None):
    if arg is None and text is None:
        embed = discord.Embed(title = "Command description:", description='!changestatus `<type>` `<title>`\ntype = `watch`, `listen`, `play`, `compet`, `stream`\ntitle = Anything you want\n!changestatus compet Owm competition')
        await ctx.send(embed = embed)
        return
    elif text == None:
        await ctx.send("Please indicate the activity type\n`watch`, `listen`, `play`, `compet`, `stream`")
        return
    elif arg == 'watch':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
    elif arg == 'listen':
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))
    elif arg == 'play':
        await client.change_presence(activity=discord.Game(name=text))
    elif arg == 'compet':
        await client.change_presence(activity = discord.Activity(type=discord.ActivityType.competing, name=text))
    elif arg == 'stream':
        await ctx.send("Enter the url of __twitch__ stream:")
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        try:
            message = await client.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Cooldown is up!")
        else:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=text, url=message.content)) 
    await ctx.send(f"Changed the bot presence status as **{arg}ing {text}**!")

TOKEN = os.getenv("TOKEN")
client.run("OTIxMDQ1MTgyNjcyMTY2OTQy.YbtMKw._iqa3BMxKAvZsF3tuIk8RiVkUHE")