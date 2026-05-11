from discord.ext import commands
from discord import app_commands
import discord
import pandas as pd
import math
from ui.button import buttin
from utility.BirthDay import BirthDayAPI
from gtts import gTTS
import subprocess
import os
import tempfile
import shutil
import asyncio
from typing import List
import time
from setup import config

class birthdayAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot:commands.Bot = bot
        self.limitPerPage = 10
        self.vc_last_play  = {}
        self.COOLDOWN = 7200

    @app_commands.command(name="birthday",description="get birthday of the cs member")
    async def birthday(self,interaction:discord.Interaction):
        await interaction.response.defer()
        data = await BirthDayAPI.getdata()
        
        page = math.ceil(data.shape[0] / self.limitPerPage)
        if page == 0:
            page = 1
        pages = []
        for i in range(page):
            embed = discord.Embed(title="Birth Day Countdown!!",color=0xFFFFFF)
            start = i*self.limitPerPage
            persons:pd.DataFrame = data.iloc[start:start+self.limitPerPage]
            if i == 0:
                first = data.iloc[0]
                if first['diff'] == 0:
                    embed.add_field(name=f"Today is **{first['nickname']}** Birthday!! ",value=f"**`Claps to {first['nickname']}`**")
                embed.add_field(name="Next",value=f"**` {first['nickname']} `** In **` {first['diff']} `** days",inline=False)
            fmt = "\n".join(
                f"{(idx + 1) + start}. {row.nickname} — {row.birthday.strftime('%b %d, %Y')} "
                f"({row.diff} days left)"
                for idx, row in enumerate(persons.itertuples(index=False))
            )
            embed.add_field(name="Upcoming",value=f"`{fmt}`",inline=False)
            pages.append(embed)
                
        view = buttin(pages,None,interaction)
        view.interaction = interaction
        await interaction.followup.send(embed=pages[0], view=view)

    def format_names(self,names: list[str]) -> str:
        if len(names) <= 1:
            return names[0] if names else ""

        return ", ".join(names[:-1]) + " และ " + names[-1]

    async def generateAudioFIle(self,temp_dir:str,names:List[str]):
        texts = [
            "สวัสดีค่ะ",
            f"วันนี้เป็นวันเกิด {self.format_names(names)}",
            "เย้ๆๆๆ",
            "ย้าหู้ววว"
        ]
        files = []

        for i, text in enumerate(texts):
            path = os.path.join(temp_dir, f"part{i}.mp3")
            gTTS(text, lang="th", slow=False).save(path)
            files.append(path)

        list_path = os.path.join(temp_dir, "list.txt")

        with open(list_path, "w", encoding="utf-8") as f:
            for file in files:
                f.write(f"file '{file}'\n")
                
        output_path = os.path.join(temp_dir, "output.mp3")

        await asyncio.to_thread(subprocess.run, [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_path,
            "-c", "copy",
            output_path
        ])
        return output_path


    @commands.Cog.listener()
    async def on_voice_state_update(self, member:discord.Member, before, after):
        channel:discord.VoiceChannel = after.channel
        if not (member.guild.id == int(config["BIRTHDAY_VOICE_NOTIFY_GUILD"])):
            return

        if not (before.channel is None and after.channel is not None):
            return
        
        if member == self.bot.user or member.bot:
           return
        
        last = self.vc_last_play.get(channel.id)
        now = time.time()

        if last and now - last < self.COOLDOWN:
            return

        if len(after.channel.members) < int(config["BIRTHDAY_MEMBER_COUNT_THRESHOLD"]):
            return
        
        self.vc_last_play[channel.id] = now

        birth:pd.DataFrame = await BirthDayAPI.getBirthDayToday()
        if(birth.shape[0] == 0):
            return

        vc = channel.guild.voice_client

        if vc and vc.is_connected():
            return
        
        temp_dir = tempfile.mkdtemp()
        names = []
        for _,person in birth.iterrows():
            names.append(person['nickname'])

        output = await self.generateAudioFIle(temp_dir,names)

        if vc and vc.is_connected():
            return
        vc = await channel.connect()

        try:
            source = discord.FFmpegPCMAudio(output)
            vc.play(source)
        finally:
            while vc.is_playing():
                await asyncio.sleep(0.5)
            vc.stop()
            await vc.disconnect()
            shutil.rmtree(temp_dir)
            

       
        

        

async def setup(bot):    
  await bot.add_cog(birthdayAPI(bot))   