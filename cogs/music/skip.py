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

class skipAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot
    
    @app_commands.command(name="skip", description="Skip music")
    @app_commands.describe(to="Skip to given music")
    async def skip(self, interaction: discord.Interaction, to: Optional[int] = False):
        await interaction.response.defer()
        if await check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            if to:
                if to > len(vc.queue) or to < 1:
                    embed = embed_fail(interaction, "Please check music index again.")
                    await interaction.followup.send(embed=embed,ephemeral=True)
                    return
                wanted = vc.queue[to-1]
                vc.queue.delete(to-1)
                vc.queue.put_at(0,wanted)
                await vc.skip()
                embed = embed_success(interaction, "Skiped current song to the {} song.",to)
                await interaction.followup.send(embed=embed,ephemeral=True)
            else:
                await vc.skip()
                embed = embed_success(interaction, "Skipped ✅")
                await interaction.followup.send(embed=embed,ephemeral=True)
    

            
async def setup(bot):    
  await bot.add_cog(skipAPI(bot))  