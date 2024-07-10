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
from typing import Optional

class shuffleAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot
    
    @app_commands.command(name="shuffle", description="Shuffle music queue")
    async def shuffle(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc: wavelink.Player = interaction.guild.voice_client
        if await check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            vc.queue.shuffle()
            embed = embed_success(interaction, "Queue shuffled ✅")
            await interaction.followup.send(embed=embed,ephemeral=True)
            
async def setup(bot):    
  await bot.add_cog(shuffleAPI(bot))  