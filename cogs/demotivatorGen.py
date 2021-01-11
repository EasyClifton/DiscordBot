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

    allowedExtensions = (".jpg", ".jpeg", ".png", ".webp", ".gif")

    if ctx.message.attachments: # if message has an attachment(s)

      #Get attachment list from message attachments, get the first image in list, then stringify it's name
      filename = str(ctx.message.attachments[0].filename)

      #Check if image is in allowed format
      if filename.endswith(allowedExtensions):

        # open image
        img = Image.open("cogs/sourceImage.jpg")

        # border color
        color = "white"

        # top, right, bottom, left
        border = (5, 5, 5, 5)

        new_img = ImageOps.expand(img, border = border, fill = color)

        # save new demotivator
        new_img.save("cogs/demotivator.jpg")

        # Send demotivator
        
        await ctx.send(file = discord.File("cogs/demotivator.jpg"))

      else:

        await ctx.send("Image format not supported by Discord.")

    else:

      await ctx.send("Please attach an image!")

      

  # Errors

  @demotivator.error
  async def demotivator_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("Please provide at least one caption for the demotivator!")


def setup(client):
  client.add_cog(DemotivatorGen(client))