import wavelink as wavelink
from discord.ext import commands
import requests
import discord
from discord import app_commands
from discord.app_commands import Choice
import asyncio
from ui.embed_gen import embed_fail
from cogs.music.ui.controlpanal import *
from cogs.music.ui.nowplaying import nowplaying
from urllib.parse import urlparse
from cogs.music.createsource import createsource
from typing import List

class playAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot
        self.replacer = "$^"
        self.replacement = "."

    def is_url(self,url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
        
    async def statistic(self, search:str):
        search = search.replace(self.replacement, self.replacer)
        if len(search) > 99:
            return
        
        if self.is_url(search):
            return
        
        database = self.bot.mango["searchstatistic2"]
        data = database.find_one({"music": search})
        if not data:
            database.insert_one({"music": search, "times": 1})
        else:
            database.update_one({"music": search}, {"$inc": {"times": 1}})

    async def addtoqueue(self, track:wavelink.Playable|wavelink.Playlist, interaction, playlist=False, number=None,playlist_title=None):
        if isinstance(track,wavelink.Playlist):
            number = len(track.tracks)
            playlist_title = track.name
            track = track.tracks[0]
            playlist = True
            
        if not playlist:
            embed = discord.Embed(
                title=track.title,
                description=f"has been added to the queue ✅",
                color=0x19AD3B,
            )
            embed.set_footer(
                text=f"{interaction.user.name} added the song to the queue.",
                icon_url=interaction.user.avatar.url,
            )
            embed.set_thumbnail(url=track.artwork)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
        else:
            embed = discord.Embed(
                title=f"Add playlist `{playlist_title}` {number} song.",
                description=f"{respound.get('added')} ✅",
                color=0x19AD3B,
            )
            embed.set_footer(
                text=f"{interaction.user.name} added the song to the queue.",
                icon_url=interaction.user.avatar.url,
            )
            embed.set_thumbnail(url=track.artwork)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()

    @app_commands.command(name="play", description="play music")
    @app_commands.describe(search="Music name")
    async def play(self, interaction: discord.Interaction, search: str):
        await interaction.response.defer()

        if not interaction.user.voice:
            embed = embed_fail(interaction,"❌ You are not currently in voice channel")
            await interaction.followup.send(embed=embed,ephemeral=True)
            return
        
        elif not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)

        elif interaction.guild.voice_client.channel != interaction.user.voice.channel:
            embed = embed_fail(interaction,"❌ Bot is now used by others voice channel")
            await interaction.followup.send(embed=embed,ephemeral=True)
            return
        
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await interaction.guild.change_voice_state(channel=interaction.user.voice.channel, self_mute=False, self_deaf=True)

        await self.statistic(search)

        if not vc.playing and not vc.queue:
            setattr(vc, "np", None)
            setattr(vc, "loop", "False")
            setattr(vc, "task", None)
            setattr(vc, "Myview", None)
            setattr(vc, "interaction", interaction)
            pre = pr(interaction,nowplaying.np)
            pl = pp(interaction,nowplaying.np)
            loop = lo(interaction,nowplaying.np)
            skip = sk(interaction,nowplaying.np)
            # voldown = dw(interaction)
            # volup = uw(interaction)
            # clear = cl(interaction)
            auto = au(interaction,nowplaying.np)
            disconnect = dc(interaction,nowplaying.np)
            vc.Myview = View(timeout=None)
            vc.Myview.add_item(loop)
            vc.Myview.add_item(auto)
            vc.Myview.add_item(pre)
            vc.Myview.add_item(pl)
            vc.Myview.add_item(skip)
            # vc.Myview.add_item(voldown)
            # vc.Myview.add_item(volup)
            # vc.Myview.add_item(clear)
            vc.Myview.add_item(disconnect)
            vc.autoplay = wavelink.AutoPlayMode.partial

        vc.interaction = interaction
        # -------Lplaylist
        yt = False
        if "onlytube" in search:
            yt = True
            search = search.replace("onlytube", "")
        track = await createsource.searchen(self, search, interaction.user, onlyyt=yt)
        if track == None:
            embed = embed_fail(interaction, "The song you searched doesn't exist, try another song.")
            await interaction.followup.send(embed=embed,ephemeral=True)
            return
        
        if not vc.playing and not vc.queue:
            await vc.queue.put_wait(track)
            await vc.set_volume(100)
            await vc.play(await vc.queue.get_wait(),populate=True)
            print(f"playing {vc.current} requested by {vc.current.extras.requester}")
        else:
            await vc.queue.put_wait(track)
            print(f'adding {track}')
            await self.addtoqueue(track, interaction)
            await nowplaying.np(self, interaction)

    @play.autocomplete("search")
    async def fruits_autocomplete(
        self,
        interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        database = self.bot.mango["searchstatistic2"]
        source = database.find().sort("times", -1).limit(3)
        if len(current) > 0:
            source = database.find({"music": {"$regex": current,'$options' : 'i'}}).limit(25)
        return [app_commands.Choice(name=l["music"].replace(self.replacer, self.replacement),value=l["music"].replace(self.replacer, self.replacement))for l in source]
async def setup(bot):    
  await bot.add_cog(playAPI(bot))  