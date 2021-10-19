import discord
from discord.ext import commands
import typing


class Talking(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events

    @commands.Cog.listener()
    async def on_ready(self):
        print("Extension \"Talking\" active!")

    # Commands

    @commands.command(brief="Makes the bot say something")
    async def say(self, ctx, *, messageText):  # add optional channel
        await ctx.message.delete()
        await ctx.send(messageText)  # channel

    @commands.command(brief="Makes the bot edit any of it's messages")
    async def edit(self, ctx, message: discord.Message, *, messageText):
        await ctx.message.delete()
        await message.edit(content=messageText)

    @commands.command(brief="Makes the bot reply to any message")
    async def reply(self, ctx, message: discord.Message, pingAuthor: typing.Optional[bool] = True, *, messageText):
        await ctx.message.delete()
        await message.reply(content=messageText, mention_author=pingAuthor)

    @commands.command(aliases=["del"], brief="Deletes a specific message")
    async def delete(self, ctx, messageToDelete: discord.Message):
        await ctx.message.delete()
        await messageToDelete.delete()



    # Errors

    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please provide the {error.param} argument!")

    @edit.error
    async def edit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please provide the \"{error.param}\" argument!")
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"The \"{error.param}\" must be a number!")


def setup(client):
    client.add_cog(Talking(client))
