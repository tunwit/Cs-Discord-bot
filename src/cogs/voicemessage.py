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

class voicemessageAPI(commands.Cog):
    pass


async def setup(bot):    
  await bot.add_cog(voicemessageAPI(bot))   