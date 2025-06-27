import discord
from discord.ext import commands
from discord import app_commands
import json
from discord.app_commands import Choice
from typing import List
from datetime import datetime
import time

class echoAPI(commands.Cog):
    def __init__(self, bot):
         self.bot:commands.Bot = bot
         self.invites = self.bot.invites
        
    @app_commands.command(name="echo",description="echo echo echo")
    async def echo(self,interaction:discord.Interaction): 
        vc = await interaction.user.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio('/Users/littlebirdd/Desktop/project/csbot/src/isus.mp3'))
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()
async def setup(bot):    
  await bot.add_cog(echoAPI(bot))   
