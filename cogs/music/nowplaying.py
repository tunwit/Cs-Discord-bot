import wavelink as wavelink
from discord.ext import commands
import discord
from discord import app_commands
from cogs.music.ui.controlpanal import *
from cogs.music.eventmanager import eventManager

class nowplayingAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot

    async def check_before_play(self,interaction: discord.Interaction):
        vc: wavelink.Player = interaction.guild.voice_client
        if vc == None:
            embed = embed_fail(interaction,"❌ Bot is currently not in the voice channel.")
            await interaction.followup.send(embed=embed)
            return False
        if interaction.user.voice == None:
            embed = embed_fail(interaction,"❌ You are not currently in voice channel")
            await interaction.followup.send(embed=embed)
            return False
        if interaction.guild.voice_client.channel != interaction.user.voice.channel:
            embed = embed_fail(interaction,"❌ Bot is now used by others voice channel")
            await interaction.followup.send(embed=embed)
            return False
        return True
    
    @app_commands.command(name="nowplaying", description="Show current music")
    async def nowplaying(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            try:
                vc.task.cancel() # To prevent bot from send Nowplaying message twice
            except:
                pass
            vc.task = self.bot.loop.create_task(eventManager.current_time(self,vc.interaction))

async def setup(bot):    
  await bot.add_cog(nowplayingAPI(bot))  