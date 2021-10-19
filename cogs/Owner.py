import discord
import typing
import asyncio
from discord.ext import commands
from datetime import datetime

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events

    @commands.Cog.listener()
    async def on_ready(self):
        print("Extension \"Owner\" active!")


    # Commands

    @commands.command()
    async def status(self, ctx, status):
        await self.client.change_presence(status=discord.Status.status)
        await ctx.send(f"Successfully set status to \"{status}\".")

    @commands.command()
    async def activity(self, ctx, *, activity):
        await self.client.change_presence(activity=discord.Game(activity))
        await ctx.send(f"Successfully set activity to \"{activity}\".")

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
      await ctx.send("Restarting, allow up to 5 seconds...")
      now = datetime.now()
      print(f"[{now}] Restarting...")
      await self.client.logout()

    @commands.command(brief="Renames a specific user")
    @commands.is_owner()
    async def rename(self, ctx, member: discord.Member, *, name):
      await member.edit(nick=name)
      await ctx.message.delete()

      '''
      if name is None:
        await member.edit(nick=None)
      else:
        await member.edit(nick=name)
        await ctx.message.delete()
      '''

    @commands.command(brief="Renames everyone in the guild")
    @commands.is_owner()
    async def renameall(self, ctx, *, name):
      members = ctx.guild.members
      print(members)
      for member in members:
        await asyncio.sleep(5)
        print(member)
        await member.edit(nick=name)

    @commands.command(aliases=["eval"])
    @commands.is_owner()
    async def evaluate(ctx, *, command):
        await ctx.send(eval(command))
        

    # Errors

    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have permissions to use this command. You need the {error.missing_perms} permission(s) to execute this command.")
        if isinstance(error, commands.NotOwner):
            await ctx.send("Only the owner of the bot can exectue this command!")

    @activity.error
    async def activity_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide the activity to set!")
    
    

def setup(client):
    client.add_cog(Owner(client))