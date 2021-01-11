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

      # Set base attachment varible
      attachment = ctx.message.attachments[0]

      # Stringify the image's name
      sourceImageName = str(attachment.filename)

      #Check if image is in an allowed format
      if sourceImageName.endswith(allowedExtensions):

        # Download image from Discord
        #This refused to work so I used requests instead. I will probably revisit this in the future.
        await attachment.save(f"/cogs/demotivators/{sourceImageName}/", seek_begin = False, use_cached = False)
        
        # open image
        sourceImage = Image.open(f"cogs/demotivators/{sourceImageName}/")

        # border color
        color = "white"

        # top, right, bottom, left
        border = (5, 5, 5, 5)

        demotivator = ImageOps.expand(sourceImage, border = border, fill = color)

        # save new demotivator
        demotivator.save(f"cogs/demotivators/{sourceImageName}/")

        # Send demotivator
        
        await ctx.send(file = discord.File(f"cogs/demotivators/{sourceImageName}/"))

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