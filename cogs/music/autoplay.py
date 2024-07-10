import wavelink as wavelink
from discord.ext import commands
import discord
from discord import app_commands
from cogs.music.ui.controlpanal import *
from cogs.music.eventmanager import eventManager
from cogs.music.utility.check_before_play import check_before_play
from cogs.music.ui.nowplaying import nowplaying
from ui.embed_gen import embed_success

class autoplayAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot
    
    @app_commands.command(
        name="autoplay",
        description="when ran out of music bot will random music for you",
    )
    async def autoplay(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            au = [x for x in vc.Myview.children if x.custom_id == "au"][0]
            if vc.autoplay == wavelink.AutoPlayMode.partial:
                vc.autoplay = wavelink.AutoPlayMode.enabled
                au.style = discord.ButtonStyle.green
            elif vc.autoplay == wavelink.AutoPlayMode.enabled:
                vc.autoplay = wavelink.AutoPlayMode.partial
                au.style = discord.ButtonStyle.gray
            await nowplaying.np(self, interaction)
            embed = embed_success(interaction, "Autoplay successfully enabled")
            await interaction.followup.send(embed=embed,ephemeral=True)
            
async def setup(bot):    
  await bot.add_cog(autoplayAPI(bot))  