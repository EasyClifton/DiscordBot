import discord
from discord.ext import commands
import PIL
from PIL import Image, ImageOps
import math


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

      #Check if image is in an allowed format
      if attachment.filename.endswith(allowedExtensions):

        # Download image from Discord and save it with the correct file name and extension
        await attachment.save(f"./cogs/demotivators/{attachment.filename}")
        
        # Open image
        discordImage = Image.open(f"./cogs/demotivators/{attachment.filename}")

        # Resize image to fit base
        discordImage.thumbnail((600, 600))

        # Set color
        color = "black"

        # Top, right, bottom, left
        border = (4, 4, 4, 4)

        # Make first border
        discordImage = ImageOps.expand(discordImage, border = border, fill = color)

        # Set new color
        color = "white"

        # Make second border
        discordImage = ImageOps.expand(discordImage, border = border, fill = color)

        # Open the background image and copy it
        pasteBaseToCopy = Image.open("./cogs/pasteBase.png")

        pasteBase = pasteBaseToCopy.copy()

        # Calculate the values to paste the discordImage into the center of the paste base
        imgWidth, imgHeight = discordImage.size

        # Center the image
        xCoord = int(math.floor((1000 - imgWidth) / 2))
        yCoord = int(math.floor((700 - imgHeight) / 2))

        # Paste the discordImage to the paste base
        pasteBase.paste(discordImage, (xCoord, yCoord, xCoord + imgWidth, yCoord + imgHeight))

        # Save the newly made demotivator
        pasteBase.save(f"./cogs/demotivators/{attachment.filename}")

        # Send demotivator
        await ctx.send(file = discord.File(f"./cogs/demotivators/{attachment.filename}"))

      else:

        await ctx.send("This image format not supported by Discord.")

    else:

      await ctx.send("Please attach an image!")

      

  # Errors

  @demotivator.error
  async def demotivator_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("Please provide at least one caption for the demotivator!")


def setup(client):
  client.add_cog(DemotivatorGen(client))