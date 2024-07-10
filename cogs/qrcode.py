import discord
from discord.ext import commands
from discord import app_commands,File
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import io

class qrcodeAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot

    @app_commands.command(name="qrcode",description="generate qr code")
    async def qrcode(self,interaction:discord.Interaction,text:str) :
        await interaction.response.defer()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=1,
        )
        qr.add_data(text)
        img = qr.make_image(image_factory=StyledPilImage, embeded_image_path="round.png",
                      color_mask=RadialGradiantColorMask(center_color=((3, 1, 51)),edge_color=((27, 12, 69))),
                      eye_drawer=RoundedModuleDrawer(radius_ratio=1))
        with io.BytesIO() as image_binary:
            img.save(image_binary, format="PNG")
            image_binary.seek(0)
            await interaction.followup.send(
                content=f"This is QR CODE for ` {text} ` ",
                file=File(fp=image_binary, filename="image.png"),
            )

async def setup(bot):    
  await bot.add_cog(qrcodeAPI(bot))  
