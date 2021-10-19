import discord
from discord.ext import commands
import PIL
from PIL import Image, ImageOps, ImageFont, ImageDraw
import math


class MemeStuff(commands.Cog, name='Meme stuff'):
    def __init__(self, client):
        self.client = client

    # Events

    @commands.Cog.listener()
    async def on_ready(self):
        print('Extension "Meme Stuff" active!')

    # Commands

    @commands.command(aliases = ["dem"], brief = "Creates a demotivator with one or two captions", description = "Creates a demotivator with one or two captions. USAGE: .demotivator \"Caption 1\" \"Caption 2\" (Caption 2 is optional)")

    async def demotivator(self, ctx, caption1, caption2 = None):

        allowedExtensions = (".jpg", ".jpeg", ".png", ".webp", ".gif")

        if ctx.message.attachments:  # if message has an attachment(s)

            # Set base attachment varible
            attachment = ctx.message.attachments[0]

            #Check if image is in an allowed format
            if attachment.filename.lower().endswith(allowedExtensions):

                # Download image from Discord and save it with the correct file name and extension
                await attachment.save(
                    f"./cogs/demotivators/{attachment.filename}")

                # Open image
                discordImage = Image.open(
                    f"./cogs/demotivators/{attachment.filename}")

                # Resize image to fit base
                discordImage.thumbnail((600, 600))

                # Set color
                color = "black"

                # Top, right, bottom, left
                border = (4, 4, 4, 4)

                # Make first border
                discordImage = ImageOps.expand(discordImage, border=border, fill=color)

                # Set new color
                color = "white"

                # Make second border
                discordImage = ImageOps.expand(discordImage, border=border, fill=color)

                # Create the background image
                pasteBase = Image.new("RGB", (1000, 1000),"black")

                # Calculate the values to paste the discordImage into the center of the paste base
                imgWidth, imgHeight = discordImage.size

                # Center the image
                xCoord = int(math.floor((1000 - imgWidth) / 2))
                yCoord = int(math.floor((700 - imgHeight) / 2))

                # Paste the discordImage to the paste base
                pasteBase.paste(discordImage,(xCoord, yCoord, xCoord + imgWidth, yCoord + imgHeight))

                # Add the captions

                draw = ImageDraw.Draw(pasteBase)

                fontSize = min(round((1000/len(caption1))*1.5), 100)
                
                # print(fontSize)
                
                # font = ImageFont.truetype(<font-file>, <font-size>)
                # Impact is for memes "./cogs/impact.ttf"
                font = ImageFont.truetype(font = "./cogs/assets/times.ttf", size = fontSize)
                # Calculate position for text
                captionWidth, captionHeight = draw.textsize(caption1, font = font)

                # draw.text((x, y),"Sample Text",(r,g,b))
                draw.text(((1000 - captionWidth) / 2, 750), caption1, (255, 255, 255), font = font)
        
                # Save the newly made demotivator
                pasteBase.save(f"./cogs/demotivators/{attachment.filename}")

                # Send demotivator
                await ctx.send(file=discord.File(f"./cogs/demotivators/{attachment.filename}"))

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
    client.add_cog(MemeStuff(client))