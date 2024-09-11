from discord.ext import commands
from discord import app_commands
import discord
import requests
from bs4 import BeautifulSoup
import datetime
from ui.button import buttin
import math
import itertools

class birthdayAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot

    async def getdata(self):
        html = requests.get('https://docs.google.com/spreadsheets/d/1KVJLEbZzuSDzwCVVm_5r0e9JEi1Kppr8l3r1Z2Qk44E/gviz/tq?tqx=out:html&tq&gid=1').text
        soup = BeautifulSoup(html, 'lxml')
        raw = soup.find_all('table')[0]
        rows = raw.find_all('tr')
        result = {}
        for i in range(1,len(rows)):
            row = rows[i].find_all('td')
            date = datetime.datetime.strptime(row[3].text,'%d/%m/%Y')
            result_ = datetime.date(date.year,date.month,date.day)
            today = datetime.date.today()
            diff = datetime.date(today.year,result_.month,result_.day) - datetime.date(today.year,today.month,today.day)
            info = {
                    "create_at":row[0].text,
                    "name":row[1].text,
                    "nickname":row[2].text,
                    "birthday":row[3].text,
                    "ig":row[4].text,
                    "name_eng":row[5].text,
                    "nickname_eng":row[6].text,
                    "diff":diff
            }
            result.update({info['name_eng']:info})

        return result


    async def sort_date(self,data:dict):
        result_positive = {}
        result_negative = {}
        newdata = data.copy()
        while newdata:
            min_ = newdata[list(newdata)[0]]['diff'].days
            p = newdata[list(newdata)[0]]['name_eng']
            for person in newdata:
                diff = newdata[person]["diff"].days
                if diff < min_:
                    min_ = diff
                    p = person
            if min_ < 0:
                newdata[p]["diff"] = datetime.timedelta(days=min_+365)
                result_negative.update({p:newdata[p]})
            else:
                result_positive.update({p:newdata[p]})
            newdata.pop(p)
        result_positive.update(result_negative)
        return result_positive

    @app_commands.command(name="birthday",description="get birthday of the cs member")
    async def birthday(self,interaction:discord.Interaction):
        await interaction.response.defer()
        data = await self.getdata()
        sort = await self.sort_date(data)
        page = math.ceil(len(sort) / 10)
        if page == 0:
            page = 1
        pages = []
        for i in range(page):
            embed = discord.Embed(title="Birth Day Countdown!!",color=0xFFFFFF)
            persons = list(itertools.islice(sort, 0, 10))
            if i == 0:
                first = sort[list(sort)[0]]
                if first['diff'].days == 0:
                    embed.add_field(name=f"Today is **{first['nickname']}** Birthday!! ",value=f"**`Claps to {first['nickname']}`**")
                embed.add_field(name="Next",value=f"**` {first['nickname']} `** In **` {first['diff'].days} `** days",inline=False)
                
            fmt = "\n".join(f"{j+(10*i)}. {sort[name]['nickname']} {sort[name]['birthday']} In {sort[name]['diff'].days} days" for j,name in enumerate(persons,1))
            embed.add_field(name="Upcoming",value=f"`{fmt}`",inline=False)
            for index in range(10):
                try:
                    sort.pop(list(sort)[0])
                except:pass
            pages.append(embed)
                
        view = buttin(pages,None,interaction)
        view.interaction = interaction
        await interaction.followup.send(embed=pages[0], view=view)
async def setup(bot):    
  await bot.add_cog(birthdayAPI(bot))   