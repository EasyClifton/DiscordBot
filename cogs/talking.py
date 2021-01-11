import discord
from discord.ext import commands

class Talking(commands.Cog):

  def __init__(self, client):
    self.client = client


  # Events

  @commands.Cog.listener()
  async def on_ready(self):
    print(f"Extension \"Talking\" active!")


  # Commands
    
  @commands.command()
  async def say(self, ctx, *, message): # add optional channelID
    #channel = channelID
    await ctx.send(message) # channel
    await ctx.delete(message)

  @commands.command()
  async def edit(self, ctx, channelID : int, messageID : int, content): # : discord.Channel = None
    channel = await ctx.get_channel(channelID)
    print(channel)
    message = await channel.fetch_message(messageID)
    print(message)
    await message.edit(content = content)



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