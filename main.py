import discord
from discord.ext import commands
import os
from datetime import datetime, timedelta

intents = discord.Intents().all()

client = commands.Bot(intents=intents, command_prefix=commands.when_mentioned_or("."))  #  help_command = None

# Events, general error events

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    startActivity = discord.Game("discord.py")
    startStatus = discord.Status.online
    await client.change_presence(status = startStatus, activity = startActivity)


@client.event
async def on_message(message):
    if str(client.user.id) in message.content:
        await message.channel.send("My prefix is `.`")
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You do not have permissions to use this command. You need the {error.missing_perms} permission(s) to execute this command.")
    if isinstance(error, commands.NotOwner):
        await ctx.send("Only the owner of the bot can exectue this command!")


# Cogs

@client.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully loaded \"{extension}\" extension!")

@client.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully unloaded \"{extension}\" extension!")

@client.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully reloaded \"{extension}\" extension!")



# Commands

@client.command(brief = "This is the brief description", description = "This is the full description")
async def ping(ctx):
  await ctx.send(f"🏓 Pong! {round(client.latency * 1000)}ms")

# And here comes the most complicated, overingeneered and unoptimised purge command ever


@client.command(aliases = ["clear"])
# @commands.has_permissions(manage_messages = True)
#@commands.has_permissions(administrator=True)
@commands.is_owner()

# Defining the command, the amount argument is the amount of messages that needs to be deleted and the userID is the optional ID of the user the messages of whom need to be deleted.
async def purge(ctx, amount: int, member: discord.Member = None):

  # Do a normal deletion if the userID argument is not present
  if member == None:
    await ctx.channel.purge(limit = amount + 1)

  # else do a check to find out the messages that need to be deleted. This can probaby be done 10 times easier but I'm still a programming noob so...
  else:
    # Delete the message that triggered the command
    await ctx.message.delete()
    # Calculate the time from the last two weeks and collect the message history.
    twoWeeksAgo = datetime.utcnow() - timedelta(days = 14)
    messages = await ctx.channel.history(after = twoWeeksAgo, oldest_first = False).flatten()
    messagesToDelete = []

    # Iterate through messages until the requested amount is found or the messages end and delete the collected messages afterwards
    for message in messages:
      if message.author == member:
        messagesToDelete.append(message)

      if len(messagesToDelete) == amount:
        break
    
    for message in messagesToDelete:
      await message.delete()

    if len(messagesToDelete) <= amount:
      embed = discord.Embed(description = f"<:greentick:806254855588937748> Deleted {len(messagesToDelete)} message(s). Messages older than two weeks were skipped.", colour=0x6dd94c)
      await ctx.send(embed=embed)
    else:
      print("enough")
      embed = discord.Embed(description = f"<:greentick:806254855588937748> Deleted {len(messagesToDelete)} message(s).", colour=0x6dd94c)
      await ctx.send(embed=embed)

@client.command()
async def error(ctx):
    embed = discord.Embed(description = "<:redtick:806254855143948300> Error!", colour=0xff0000)
    embed.set_image(url="https://images-ext-1.discordapp.net/external/NQYiVqmfxw7d4ICOFsQp2ygDDRykbn2ZXgHaWhwfTlo/%3Fsize%3D256%26f%3D.gif/https/cdn.discordapp.com/avatars/493040027274575883/a_0ca63bb9ef459a782b9b85dcb4524ed5.gif")
    await ctx.send(embed=embed)

@client.command()
async def embed(ctx, *, message):
  embed = discord.Embed(description=message)
  await ctx.send(embed=embed)



#@client.command()
#async def presence(ctx, status, activity): # Add a * after ctx,
#  await ctx.send(f"Status and activity set to {presence.status} and {presence.activity}")
#  await client.change_presence(status = discord.Status.status, activity = activity.activity)
#  await ctx.send(f"Status and activity set to {presence.status} and {presence.activity}")


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

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide the amount of messages to purge!")
    if isinstance(error, commands.BadArgument):
        await ctx.send("The amount of messages to purge must be a number!")



#@presence.error
#async def presence_error(ctx, error):
#  if isinstance(error, commands.MissingRequiredArgument):
#    await ctx.send(f"Please provide the {error.param} parameter(s)")

# The token is stored in an environmental variable called TOKEN

token = os.getenv("TOKEN")

client.run(token)
