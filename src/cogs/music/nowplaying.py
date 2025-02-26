import discord.ext.commands
import wavelink as wavelink
from discord.ext import commands
import discord
from discord import app_commands
from cogs.music.ui.controlpanal import *
from cogs.music.eventmanager import eventManager
from cogs.music.utility.check_before_play import check_before_play
import discord.ext

class nowplayingAPI(commands.Cog):
    def __init__(self, bot :commands.Bot):
        self.bot = bot

    @app_commands.command(name="nowplaying", description="Show current music")
    async def nowplaying(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            try:
                vc.task.cancel() # To prevent bot from send Nowplaying message twice
            except:
                pass
            vc.task = self.bot.loop.create_task(eventManager.current_time(self,vc.interaction))

async def setup(bot):    
  await bot.add_cog(nowplayingAPI(bot))  