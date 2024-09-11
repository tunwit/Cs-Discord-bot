import discord
from discord.ext import commands
from discord import app_commands
import requests
import re

class linkshortener(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot
    
    @app_commands.command(name="linkshortener",description="shorten your link")
    @app_commands.describe(url="link or url")
    async def linkshortener(self,interaction:discord.Interaction,url:str):
        await interaction.response.defer()
        regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not re.match(regex, url):
            embed=discord.Embed(description=f"This is not valid url",color=0xcc8c2d)
            embed.set_author(name=interaction.user.name,icon_url=interaction.user.display_avatar.url)
            await interaction.followup.send(embed = embed,ephemeral=True)
            return
        result = requests.post('https://littleshort.vercel.app/api/link',json={"origin":url})
        if result.status_code == 201:
            await interaction.followup.send(f'https://littleshort.vercel.app/{result.json()["data"]["uniqueID"]}')
        else:
            embed=discord.Embed(description=f"There is an error occured status code {result.status_code}",color=0xcc8c2d)
            embed.set_author(name=interaction.user.name,icon_url=interaction.user.display_avatar.url)
            await interaction.followup.send(embed = embed,ephemeral=True)

async def setup(bot):    
  await bot.add_cog(linkshortener(bot))  
