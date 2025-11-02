import pandas as pd
import datetime
import discord
import random

class BirthDayAPI:

    @staticmethod
    def _parse_birthday(date_str):
            try:
                day, month, year = map(int, date_str.split('/'))
                if year > 2500:  # Thai Buddhist year
                    year -= 543
                return pd.Timestamp(datetime.date(year, month, day))
            except Exception:
                return None
            
    @staticmethod
    def _renameColumn(df:pd.DataFrame):
        df.rename(columns={
            "วันเกิด (ex. 19/01/2005)":"birthday",
            "ชื่อ นามสกุล (ไทย)(ไม่ต้องมีคำนำหน้า)" : "fullname",
            "ชื่อเล่น (ไทย)" : "nickname"
            }, inplace=True)
        
    @staticmethod
    def _setupColumnData(df:pd.DataFrame):
        df["birthday"] = df["birthday"].apply(BirthDayAPI._parse_birthday)
        df['age'] = ((pd.Timestamp.now() - df['birthday']) / pd.Timedelta(days=365.25)).astype(int)
        df["diff"] = df.apply(BirthDayAPI._days_until_birthday,axis=1)

        df.sort_values(by=["diff","fullname"])

    @staticmethod
    def _days_until_birthday(row):
        today = datetime.date.today()
        next_birthday = datetime.date(today.year, row["birthday"].month, row["birthday"].day)
        if next_birthday < today:
            next_birthday = datetime.date(today.year + 1, row["birthday"].month, row["birthday"].day)
        return (next_birthday - today).days
    
    @staticmethod
    async def _loadData():
        url = 'https://docs.google.com/spreadsheets/d/1KVJLEbZzuSDzwCVVm_5r0e9JEi1Kppr8l3r1Z2Qk44E/gviz/tq?tqx=out:csv&tq&gid=1'
        df = pd.read_csv(url)
        BirthDayAPI._renameColumn(df)
        BirthDayAPI._setupColumnData(df)
        return df
    
    @staticmethod
    async def getBirthDayToday():
        df = await BirthDayAPI._loadData()
        birthToday = df[df['diff'] == 0] 

        return birthToday
    
    @staticmethod
    async def getdata():
        return await BirthDayAPI._loadData()
    
    @staticmethod
    def createBirthDayEmbed(person:pd.Series):
        """Generate a birthday embed for a person"""
        nickname = person.get("nickname", "เพื่อน")
        fullname = person.get("fullname", "")
        age = person.get("age", None)

        greetings = [
            f"🎉 สุขสันต์วันเกิด {nickname}! 🎂",
            f"🎈 Happy Birthday {nickname}! 🎁",
            f"✨ ขอให้ {nickname} มีความสุขมาก ๆ ในวันเกิดนี้!",
            f"🥳 HBD {nickname}! ขอให้ปีนี้เป็นปีที่ดีสุด ๆ!"
        ]

        wishes = [
            "ขอให้ทุกวันเต็มไปด้วยรอยยิ้ม 😊",
            "ขอให้มีความสุข ความสำเร็จ และสุขภาพแข็งแรง 💪",
            "ขอให้โชคดีในทุกเรื่อง และได้ทำในสิ่งที่รัก 💖",
            "ขอให้ปีนี้มีแต่โปรเจคดีๆ เข้ามา 🎊",
            "ขอให้อยู่ด้วยกันจนจบปี 4 💖"
        ]


        embed = discord.Embed(
            title=random.choice(greetings),
            description=random.choice(wishes),
            color=discord.Color.random()
        )

        # Add more context fields
        embed.add_field(name="👤 ชื่อ", value=fullname or "-", inline=True)
        if age is not None:
            embed.add_field(name="🎂 อายุ", value=f"{age} ปี", inline=True)
        embed.add_field(name="📅 วันที่", value=datetime.datetime.today().strftime("%d/%m/%Y"), inline=False)
        embed.set_footer(text="🎉 ขอให้วันนี้เป็นวันที่ดี 🎉")

        return embed
    
