import wavelink as wavelink
from wavelink import StatsResponsePayload,Player
from discord.ext import commands
import discord
from discord import app_commands
from cogs.music.ui.controlpanal import *
from cogs.music.eventmanager import eventManager
from cogs.music.utility.check_before_play import check_before_play
from cogs.music.ui.nowplaying import nowplaying
from ui.embed_gen import embed_success
from discord import ui
import json
from utility.check_is_manager import is_manager

class statAPI(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    
    @app_commands.command(
        name="stat",
        description="send all stat of the bot",
    )
    @app_commands.check(is_manager)
    async def stat(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Stat of Com sci|สาขาคนรักเเมว")
        total_guilds = len(self.bot.guilds)

        # Lavalink
        #--------------------------------
        wavelink.Node.fetch_version() #Lavalink version
        wavelink.Node.status # is connect
        lavalink_Stat:StatsResponsePayload = wavelink.Node.fetch_stats() #Lavalink Stat
        lavalink_Stat.cpu.cores
        lavalink_Stat.cpu.lavalink_load
        lavalink_Stat.memory.used
        #--------------------------------
        
        #Player
        #--------------------------------
        voice_clients:list[Player] = self.bot.voice_clients
        len(voice_clients) #total player
        for vc in voice_clients:
            vc.guild #guild
            vc.current #current track
        #--------------------------------
  

async def setup(bot):    
    
  await bot.add_cog(statAPI(bot))  