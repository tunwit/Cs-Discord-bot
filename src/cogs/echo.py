import discord
from discord.ext import commands
from discord import app_commands
import time
from ui.embed_gen import embed_fail
import wavelink as wavelink
from gtts import gTTS
import asyncio
from discord.app_commands import Choice

from io import BytesIO
class echoAPI(commands.Cog):
    def __init__(self, bot):
         self.bot:commands.Bot = bot
         self.invites = self.bot.invites
        
    @app_commands.command(name="echo",description="echo echo echo")
    @app_commands.choices(lang=[
    Choice(name = "EN",value="en"),
    Choice(name = "TH",value="th"),])
    async def echo(self,interaction:discord.Interaction,text:str,lang:str): 
        await interaction.response.defer(thinking=True)
        if not interaction.user.voice:
            embed = embed_fail(interaction,"❌ You are not currently in voice channel")
            await interaction.followup.send(embed=embed,ephemeral=True)
            return
        elif not interaction.guild.voice_client:
            vc = await interaction.user.voice.channel.connect()
        elif interaction.guild.voice_client.channel != interaction.user.voice.channel:
            embed = embed_fail(interaction,"❌ Bot is now used by others voice channel")
            await interaction.followup.send(embed=embed,ephemeral=True)
            return
        elif  isinstance(vc, wavelink.Player):
            embed = embed_fail(interaction,"❌ Bot is now used music system")
            await interaction.followup.send(embed=embed,ephemeral=True)
            return
        else:
            vc = interaction.guild.voice_client

        tts = gTTS(text=text, lang=lang)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        await interaction.followup.send(content="OK",ephemeral=True)
        try:
            
            vc.play(discord.FFmpegPCMAudio(mp3_fp,pipe=True))
        finally:
            while vc.is_playing():
                await asyncio.sleep(0.5)
            vc.stop()
            await vc.disconnect()

        


async def setup(bot):    
  await bot.add_cog(echoAPI(bot))   
