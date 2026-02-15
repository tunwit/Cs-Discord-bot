from discord.ext import commands
from discord import app_commands
import discord
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import math
from ui.button import buttin
from utility.BirthDay import BirthDayAPI

class birthdayAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot
        self.limitPerPage = 10

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
async def setup(bot):    
  await bot.add_cog(birthdayAPI(bot))   