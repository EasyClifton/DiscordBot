import discord
from discord.ext import commands
import os
import random
import re
from datetime import datetime

client = commands.Bot(command_prefix=".")  #  help_command = None

# Events, general error events

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    startActivity = discord.Game("with discord.py")
    startStatus = discord.Status.online
    await client.change_presence(status = startStatus, activity = startActivity)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("This command does not exist.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You do not have permissions to use this command. You need the {error.missing_perms} permission(s) to execute this command.")
    if isinstance(error, commands.NotOwner):
        await ctx.send("Only the owner of the bot can exectue this command!")


# Cogs

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully loaded \"{extension}\" extension!")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully unloaded \"{extension}\" extension!")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully reloaded \"{extension}\" extension!")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


# Commands

@client.command(brief = "This is the brief description", description = "This is the full description")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(client.latency * 1000)}ms")

@client.command()
async def status(ctx, status):
    await client.change_presence(status=discord.Status.status)
    await ctx.send(f"Successfully set status to \"{status}\".")


@client.command()
async def activity(ctx, *, activity):
    await client.change_presence(activity=discord.Game(activity))
    await ctx.send(f"Successfully set activity to \"{activity}\".")

@client.command()
async def save(ctx):
    attachment = ctx.message.attachments[0]
    # this will save it with the correct file extension
    await attachment.save(attachment.filename) 
    await ctx.send("File saved!")


@client.command(aliases = ["clear"])
# @commands.has_permissions(manage_messages = True)
@commands.is_owner()
async def purge(ctx, amount: int, userID: int = None):
  if userID == None:
    await ctx.channel.purge(limit = amount + 1)
  else: # Use regex to verify ID
    await ctx.message.delete()
    messageCounter = 0
    while messageCounter <= amount:
      async for message in ctx.channel.history(limit = amount):
        if message.author.id == userID:
          await message.delete()
          messageCounter += 1
          print(messageCounter)
    print("done")
    
        


@client.command()
async def embed(ctx):
    embed = discord.Embed(
        title="Title", description="Description", colour=0x4287f5)
    await ctx.send(embed=embed)

@client.command()
async def custom(ctx, *, message):
  embed = discord.Embed(description=f"{ctx.message.author.mention} {message}")
  await ctx.send(embed=embed)

@client.command(aliases=["шар", "8ball"])
async def ball(ctx, *, question):
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


#@client.command()
#async def presence(ctx, status, activity): # Add a * after ctx,
#  await ctx.send(f"Status and activity set to {presence.status} and {presence.activity}")
#  await client.change_presence(status = discord.Status.status, activity = activity.activity)
#  await ctx.send(f"Status and activity set to {presence.status} and {presence.activity}")

@client.command()
@commands.is_owner()
async def restart(ctx):
  await ctx.send("Restarting, allow up to 5 seconds...")
  now = datetime.now()
  print(f"[{now}] Restarting...")
  await client.logout()
  await client.login()
  await ctx.edit(content = "Restarted!")

# Comman-specific errors


@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide the extension to load!")

@unload.error
async def unload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide the extension to unload!")

@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide the extension to reload!")

@custom.error
async def custom_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("Please provide a message to say!")

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide the amount of messages to purge!")
    if isinstance(error, commands.BadArgument):
        await ctx.send("The amount of messages to purge must be a number!")


@activity.error
async def activity_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide the activity to set!")

@ball.error
async def ball_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please provide the question to predict the answer to!")


#@presence.error
#async def presence_error(ctx, error):
#  if isinstance(error, commands.MissingRequiredArgument):
#    await ctx.send(f"Please provide the {error.param} parameter(s)")

# The token is stored in an environmental variable called TOKEN

token = os.getenv("TOKEN")

client.run(token)
