import wavelink as wavelink
from discord.ext import commands
import discord
from discord import app_commands
from cogs.music.ui.controlpanal import *
from cogs.music.eventmanager import eventManager
from cogs.music.utility.check_before_play import check_before_play
from ui.button import buttin
import itertools
import math

class queueAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot

    @app_commands.command(name="queue", description="Send queuelist")
    async def queueList(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await check_before_play(interaction):
            pag = []
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            upcoming = vc.queue.copy()
            if vc.queue.mode == wavelink.QueueMode.loop_all:
                upcoming = (list(upcoming)+list(vc.queue.history)).copy()
            number = len(upcoming)

            page = math.ceil(number / 10)
            if page == 0:
                page = 1

            for i in range(page):
                items = list(itertools.islice(upcoming, 0, 10))
                fmt = "\n".join(f"**` {index+(10*i)}.{music}`**" for index,music in enumerate(items,1))
                if i == 0:
                    embed = discord.Embed(
                        title="There are `{more}` songs left in the queue".format(more=number - 1),
                        color=0xFFFFFF,
                    )
                    embed.add_field(
                        name="Now playing",
                        value=f"**`{vc.current.title}`**" if vc.current else "**`No song playing`**",
                        inline=False,
                    )
                    
                else: #first page
                    embed = discord.Embed(color=0xFFFFFF)

                embed.add_field(
                    name="In queue",
                    value=fmt if number else "**`There are no songs in the queue.`**",
                    inline=False,
                )
                pag.append(embed)
                for i in range(10):
                    try:
                        del upcoming[0]
                    except:
                        pass

            embed.set_footer(text="This message is not update upon playing")
            view = buttin(pag, 120, interaction)
            view.interaction = interaction
            await interaction.followup.send(embed=pag[0], view=view)

async def setup(bot):    
  await bot.add_cog(queueAPI(bot))  