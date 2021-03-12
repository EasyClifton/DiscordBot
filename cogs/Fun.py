import discord
from discord.ext import commands
import typing
import random
from datetime import datetime


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Extension \"Fun\" active!")

    # Commands

    @commands.command()
    async def vote(self, ctx, *, message):
      embed = discord.Embed(title="Голосование:", description=f"**{message}**")
      embed.set_footer(text = f"Голосование от {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
      embed.timestamp = datetime.now()
      msg = await ctx.send(embed=embed)
      await msg.add_reaction(emoji = "👍")
      await msg.add_reaction(emoji = "👎")

    @commands.command(aliases=["шар", "8ball"])
    async def ball(self, ctx, *, question):
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.",
            "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.",
            "Better not tell you now.", "Cannot predict now.",
            "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
            "My sources say no.", "Outlook not so good.", "Very doubtful."
        ]
        await ctx.send(random.choice(responses))

    @commands.command()
    async def quote(self, ctx, member: typing.Optional[discord.Member] = None, *, quote):
        await ctx.message.delete()
        embed = discord.Embed(title="Великие цитаты", description=f"> {quote}", colour=0xf8f8d9)
        if member is None:
          embed.set_footer(text = f"{ctx.message.author.display_name}#{ctx.message.author.discriminator}", icon_url=ctx.message.author.avatar_url)
        else:
          embed.set_footer(text = f"Цитата {member.display_name}#{member.discriminator}", icon_url=member.avatar_url)
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)

    #ADD THE ABILITY TO QUOTE A MESSAGE BY REFERENCIG IT

    # Errors

    @ball.error
    async def ball_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("What shall I predict?")

    @quote.error
    async def quote_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("А чё цитировать?")

def setup(client):
    client.add_cog(Fun(client))