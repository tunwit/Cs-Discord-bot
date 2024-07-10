import wavelink as wavelink
from discord.ext import commands
import discord
from discord import app_commands
from discord.app_commands import Choice
from cogs.music.ui.controlpanal import *
from cogs.music.eventmanager import eventManager
from cogs.music.utility.check_before_play import check_before_play
from cogs.music.ui.nowplaying import nowplaying
from ui.embed_gen import embed_success

class dcAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot
    
    @app_commands.command(name="disconnect", description="Leave voice chat")
    async def dc(self, interaction: discord.Interaction):
        vc: wavelink.Player = interaction.guild.voice_client
        vc.interaction = interaction
        await interaction.response.defer()
        if await check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            await self.cleanup(interaction.guild, "dc")
            embed = embed_success(interaction, "Disconnected ✅")
            await interaction.followup.send(embed=embed)

            
async def setup(bot):    
  await bot.add_cog(dcAPI(bot))  