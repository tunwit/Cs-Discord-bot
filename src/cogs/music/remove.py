import wavelink as wavelink
from discord.ext import commands
import discord
from discord import app_commands
from cogs.music.ui.controlpanal import *
from cogs.music.eventmanager import eventManager
from cogs.music.utility.check_before_play import check_before_play
from cogs.music.ui.nowplaying import nowplaying
from ui.embed_gen import embed_success

class removeAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot

    @app_commands.command(name="remove", description="Remove given music from queue")
    @app_commands.describe(index="Music Sequence")
    async def remove(self, interaction: discord.Interaction, index: int):
        await interaction.response.defer()
        if await check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            delete = None
            if vc.queue.mode == wavelink.QueueMode.loop_all:
                if index > (vc.queue.count+vc.queue.history.count) or index < 1:#Index out of range handler
                    erembed = embed_fail(interaction, "Please check the deletion index again")
                    await interaction.followup.send(embed=erembed)
                    return
                if index > vc.queue.count: 
                    delete = vc.queue.history.peek(index-len(vc.queue)-1)
                    vc.queue.history.delete(index-len(vc.queue)-1)
                else:
                    delete = vc.queue.peek(index-1)
                    vc.queue.delete(index-1)
            else:
                if index > vc.queue.count or index < 1: #Index out of range handler
                    erembed = embed_fail(interaction, "Please check the deletion index again")
                    await interaction.followup.send(embed=erembed)
                    return
                delete = vc.queue.peek(index-1)
                vc.queue.delete(index-1)
            embed = embed_success(interaction, "**`{}`** deleted",delete)
            await interaction.followup.send(embed=embed,)
            await nowplaying().np(interaction)

async def setup(bot):    
  await bot.add_cog(removeAPI(bot))  