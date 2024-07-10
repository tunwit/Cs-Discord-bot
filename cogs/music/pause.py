import wavelink as wavelink
from discord.ext import commands
import discord
from discord import app_commands
from discord.app_commands import Choice
from ui.embed_gen import embed_fail,embed_success
from cogs.music.ui.controlpanal import *
from cogs.music.ui.nowplaying import nowplaying

class pauseAPI(commands.Cog):
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

    @app_commands.command(name="resume", description="Resume music")
    async def resume(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            re = [x for x in vc.Myview.children if x.custom_id == "pp"][0]
            re.style = discord.ButtonStyle.green
            re.emoji = "<a:1_:989120454063185940>"
            await vc.pause(False)
            embed = embed_success(interaction, "Successfully resumed ▶️")
            await interaction.followup.send(embed=embed,ephemeral=True)
            
    @app_commands.command(name="pause", description="Pause music")
    async def pause(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            re = [x for x in vc.Myview.children if x.custom_id == "pp"][0]
            re.style = discord.ButtonStyle.red
            re.emoji = "<a:2_:989120456240025670>"
            await vc.pause(True)
            await nowplaying.np(self, interaction)
            embed = embed_success(interaction, "Successfully paused ⏸")
            await interaction.followup.send(embed=embed,ephemeral=True)

async def setup(bot):    
  await bot.add_cog(pauseAPI(bot))  