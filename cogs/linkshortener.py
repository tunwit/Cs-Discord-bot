import discord
from discord.ext import commands
from discord import app_commands
import requests

class linkshortener(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot

    @app_commands.command(name="hello",description="respond to use")
    async def hello(self,interaction:discord.Interaction) :
        await interaction.response.defer()
        await interaction.followup.send("Hi!")
    
    @app_commands.command(name="linkshortener",description="shorten your link")
    @app_commands.describe(url="link or url")
    async def linkshortener(self,interaction:discord.Interaction,url:str):
        await interaction.response.defer()
        result = requests.post('https://littleshort.vercel.app/api/link',json={"origin":url})
        if result.status_code == 201:
            await interaction.followup.send(f'https://littleshort.vercel.app/{result.json()["data"]["uniqueID"]}')
        else:
            await interaction.followup.send(f'There is an error occured status code {result.status_code}')


async def setup(bot):    
  await bot.add_cog(linkshortener(bot))  
