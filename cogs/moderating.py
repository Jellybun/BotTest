import discord
from discord.ext import commands
blank = "<:blank:835155831074455622>"
inv = "<:inv:864984624052305961>"

class Moderating(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['clear', 'delete'])
    async def purge(self, ctx, amount=10):
        amount = amount + 1
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def kick(self, ctx, member : discord.Member=None, *, reason = None):
        if member is None and reason is None:
            ctx.send("Please specify a member!")
            return
        embed = discord.Embed(description=f"Kicked a user {member.name}!")
        await ctx.guild.kick(member, *, reason = reason)
        await member.send(f"You have been kicked from **{ctx.guild.name}** due to {reason} reason!")
        await ctx.send(embed=embed)

    @commands.command()
    async def ban(self, ctx, member : discord.Member=None, *, reason = None):
        if member is None and reason is None:
            ctx.send("Please specify a member!")
            return
        await ctx.guild.ban(member, *, reason = reason)
        embed = discord.Embed(description=f"Banned a user {member.name}!")
        await member.send(f"You have been banned from **{ctx.guild.name}** due to {reason} reason!")
        await ctx.send(embed=embed)
        

    

def setup(client):
    client.add_cog(Moderating(client))