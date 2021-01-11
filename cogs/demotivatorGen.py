import discord
from discord.ext import commands
import PIL
from PIL import Image, ImageOps


class DemotivatorGen(commands.Cog):

  def __init__(self, client):
    self.client = client


  # Events

  @commands.Cog.listener()
  async def on_ready(self):
    print('Extension "DemotivatorGen" active!')


  # Commands
    
  @commands.command(aliases = ["dem", "demot"])
  async def demotivator(self, ctx, text1, text2 = None):

    if ctx.attachments: # if message has an attachment(s)

      # open image
      img = Image.open("cogs/sourceImage.jpg")

      # border color
      color = "white"

      # top, right, bottom, left
      border = (5, 5, 5, 5)

      new_img = ImageOps.expand(img, border=border, fill=color)

      # save new demotivator
      new_img.save("cogs/demotivator.jpg")

      # Send demotivator
      
      await ctx.send(file = discord.File("cogs/demotivator.jpg"))

    if not ctx.attachments:

      ctx.send("Please attach an image!")

      

  # Errors

  @demotivator.error
  async def demotivator_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("Please provide at least one caption for the demotivator!")


def setup(client):
  client.add_cog(DemotivatorGen(client))