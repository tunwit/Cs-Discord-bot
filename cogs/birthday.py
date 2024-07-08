from discord.ext import commands
from discord import app_commands
import discord
import requests
from bs4 import BeautifulSoup
import datetime


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
            diff = datetime.date(2024,result_.month,result_.day) - datetime.date(2024,today.month,today.day)
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
                newdata[p]["diff"] = datetime.timedelta(days=min_+345)
                result_negative.update({p:newdata[p]})
            else:
                result_positive.update({p:newdata[p]})
            newdata.pop(p)
        result_positive.update(result_negative)
        return result_positive




    @app_commands.command(name="birthday",description="get birthday of the cs member")
    async def birthday(self,interaction:discord.Interaction):
        data = await self.getdata()
        sort = await self.sort_date(data)
        for i,name in enumerate(sort,1):
            person = sort[name]
            print(f"{i}. {person['name']} {person['nickname']} {person['birthday']} In {person['diff'].days} days")

async def setup(bot):    
  await bot.add_cog(birthdayAPI(bot))   