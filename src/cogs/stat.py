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
        total_guilds = len(self.bot.guilds)
        lavalin_status = wavelink.NodeStatus.DISCONNECTED
        node:wavelink.Node = self.bot.node

        if node:
            lavalin_status = node.status
            lavalink_Stat = await node.fetch_stats()
            cores = lavalink_Stat.cpu.cores
            lavalink_load = lavalink_Stat.cpu.lavalink_load
            system_load = lavalink_Stat.cpu.system_load
            memmory_used = lavalink_Stat.memory.used*(10**-6)

        voice_clients:list[Player] = self.bot.voice_clients
        player_stat = ""
        text_limit_lenght = 17
        for vc in voice_clients:
            guild = (vc.guild.name[:text_limit_lenght] + '..') if len(vc.guild.name) > text_limit_lenght else vc.guild.name #text truncate
            music = (vc.current.title[:text_limit_lenght] + '..') if len(vc.current.title) > text_limit_lenght else vc.current.title
            player_stat+=f"{guild} | {music if music else 'No music'}\n"
        
        if player_stat != "":
            player_stat = "`" +  player_stat + "`"
        
        guilds_status = ""
        for index,guild in enumerate(self.bot.guilds,1):
            guilds_status += f" {index}. {guild.name} {guild.member_count} Members \n"

        embed = discord.Embed(
            title="Stat of Com sci | สาขาคนรักเเมว",
            description=f"Now in {total_guilds} servers",
            color=0x2945ab
            )
        
        embed.add_field(
            name="servers",
            value=f"`{guilds_status}`",
            inline=False
        )
        if lavalin_status == wavelink.NodeStatus.CONNECTED:
            embed.add_field(
                name="Lavalink", 
                value=f"Status: ` {lavalin_status.name} `\nCPU Cores: ` {cores} `\nLavalink Load: ` {lavalink_load:.6f} % `\nSystem Load: ` {system_load:.6f} % `\nMemory Used: ` {memmory_used:.2f} MB` ",
                inline=True
                )
           
            embed.add_field(
                name="Player",
                value=f"Total Player: ` {len(voice_clients)} `\n{player_stat}",
                inline=True
            )
        else:
            embed.add_field(
            name="Lavalink", 
            value=f"Status: ` {lavalin_status.name} `")

        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):    
    
  await bot.add_cog(statAPI(bot))  