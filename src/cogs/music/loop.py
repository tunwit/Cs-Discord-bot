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

trans_queueMode= {
            'wavelink.QueueMode.normal':"Disable",
            'wavelink.QueueMode.loop':"Song",
            'wavelink.QueueMode.loop_all':"Queue"
        }

class loopAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot
    
    @app_commands.command(name="loop", description="Set music loop status")
    @app_commands.describe(status="loop status")
    @app_commands.choices(
        status=[
            Choice(name="False (ปิด)", value='wavelink.QueueMode.normal'),
            Choice(name="Song (เพลง)", value="wavelink.QueueMode.loop"),
            Choice(name="Queue (ทั้งคิว)", value="wavelink.QueueMode.loop_all"),
        ]
    )
    async def loop(self, interaction: discord.Interaction, status: str):
        await interaction.response.defer()
        if await check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            vc.queue.mode = eval(status)
            lo = [x for x in vc.Myview.children if x.custom_id == "lo"][0]
            if vc.queue.mode == wavelink.QueueMode.normal:
                lo.style = discord.ButtonStyle.gray
            elif vc.queue.mode == wavelink.QueueMode.loop:
                lo.style = discord.ButtonStyle.blurple
            elif vc.queue.mode == wavelink.QueueMode.loop_all:
                lo.style = discord.ButtonStyle.green
            await nowplaying().np(interaction)
            embed = embed_success(interaction, "Switch loop to **` {} `** successfull",trans_queueMode[status])
            await interaction.followup.send(embed=embed,ephemeral=True)

            
async def setup(bot):    
  await bot.add_cog(loopAPI(bot))  