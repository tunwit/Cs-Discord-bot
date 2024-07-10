import wavelink as wavelink
from discord.ext import commands
import requests
import discord
from cogs.music.ui.nowplaying import nowplaying
from ui.embed_gen import embed_fail,embed_info
import asyncio
from async_timeout import timeout
from cogs.music.utility.cleanup import cleanup

class eventManager(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot
        self.nosongtime = 30
        self.alonetime = 25
    
    async def current_time(self, interaction):
        vc: wavelink.Player = interaction.guild.voice_client
        try:
            await vc.np.delete()
        except:pass
        vc.np = None
        while True:
            vc: wavelink.Player = interaction.guild.voice_client
            if interaction.is_expired():
                try:
                    vc.task.cancel()
                except:pass
            elif not interaction.is_expired() and vc.task.cancelled(): # resume update nowplaying after get new interaction
                vc.task = self.bot.loop.create_task(self.current_time(vc.interaction))
            try:
                np = await nowplaying.np(self,interaction)
            except discord.errors.NotFound as e:
                break
            if vc == None:
                break
            if vc.np == None:
                break
            await asyncio.sleep(9)
            await asyncio.sleep(1)
        vc.task.cancel()

    async def nosong(self, interaction:discord.Interaction):
        i=0
        while True:
            vc: wavelink.Player = interaction.guild.voice_client
            if vc.queue or vc.current:
                break
            i+=1
            print(f'counting no song {interaction.guild.name} | {i}')
            await asyncio.sleep(0.4)

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload:wavelink.payloads.TrackStartEventPayload):
        vc: wavelink.Player = payload.player
        if not vc:
            return
        if not dict(vc.current.extras).get('requester',None):
            vc.current.extras = {'requester': 'Recommended','requester_icon' : payload.player.client.user.avatar.url}
        print(f"Now playing : {vc.current}")
        await asyncio.sleep(0.3)
        vc.task = self.bot.loop.create_task(self.current_time(vc.interaction))

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload:wavelink.payloads.TrackEndEventPayload):
        print(f"ending: {payload.track}")
        vc: wavelink.Player = payload.player
        if not vc:
            return
        vc.task.cancel()
        try:
            await vc.np.delete()
        except:
            pass
        vc.np = None
        if payload.player == None:
            return
        interaction = payload.player.interaction
        if not vc.queue and vc:
            try:
                async with timeout(self.nosongtime):
                    await self.nosong(interaction)
            except:
                await cleanup(interaction.guild, "trackend")
                embed = embed_info(vc.interaction, "No more songs added, I'll be disconnect")
                try:
                    d = await interaction.followup.send(embed=embed)
                    await asyncio.sleep(5)
                    await d.delete()
                except:
                    pass
                return
 
async def setup(bot):    
  await bot.add_cog(eventManager(bot))  