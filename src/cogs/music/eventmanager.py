import wavelink as wavelink
from discord.ext import commands
import requests
import discord
from cogs.music.ui.nowplaying import nowplaying
from ui.embed_gen import embed_fail,embed_info
import asyncio
from async_timeout import timeout
from cogs.music.utility.cleanup import cleanup
from cogs.music.utility.checkdc import checkdc
from cogs.music.utility.nosong import nosong

class eventManager(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot
        self.nosongtime = 25
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
                np = await nowplaying().np(interaction)
            except discord.errors.NotFound as e:
                break
            if vc == None:
                break
            if vc.np == None:
                break
            await asyncio.sleep(10)
        vc.task.cancel()

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
    async def on_wavelink_track_exception(self, payload:wavelink.TrackExceptionEventPayload):
        vc: wavelink.Player = payload.player
        interaction = payload.player.interaction
        if not vc:
            return
        await cleanup(vc.guild, "trackend")
        embed = embed_fail(interaction, payload.exception['message'])
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()

    @commands.Cog.listener()
    async def on_wavelink_track_stuck(self, payload: wavelink.TrackStuckEventPayload):
        vc: wavelink.Player = payload.player
        interaction = payload.player.interaction
        if not vc:
            return
        await cleanup(vc.guild, "trackend")
        embed = embed_fail(interaction, "Something wrong when playing this Track, Try again late")
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        
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
                    await nosong(interaction)
            except Exception as e:
                print(e)
                await cleanup(interaction.guild, "trackend")
                embed = embed_info(vc.interaction, "No more songs added, I'll be disconnect")
                try:
                    d = await interaction.followup.send(embed=embed)
                    await asyncio.sleep(5)
                    await d.delete()
                except:
                    pass
                return

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        vc: wavelink.Player = member.guild.voice_client
        if member == self.bot.user:
            return
        if not vc:
            return
        if before.channel != after.channel:
            if after.channel == vc.channel:
                return
            if after.channel != vc.channel:
                if len(vc.channel.members) <= 1:
                    lastone = member
                    try:
                        async with timeout(self.alonetime):
                            await checkdc(member)
                            pass
                    except asyncio.TimeoutError:
                        await cleanup(member.guild, "voiceupdate no one")
                        embed=discord.Embed(description="No one is listening. I'll be disconnect. ⭕️",color=0x3495c2)
                        embed.set_author(name=member.name,icon_url=member.display_avatar.url)
                        try:
                            d = await vc.interaction.followup.send(embed=embed)
                            await asyncio.sleep(5)
                            await d.delete()
                        except:
                            pass
                        return
                    return
                
async def setup(bot):    
  await bot.add_cog(eventManager(bot))  