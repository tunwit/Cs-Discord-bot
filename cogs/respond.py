import discord
from discord.ext import commands
from discord import app_commands

class respond(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot

    @app_commands.command(name="hello",description="respond to use")
    async def hello(self,interaction:discord.Interaction) :
        await interaction.response.defer()
        await interaction.followup.send("Hi!")

async def setup(bot):    
  await bot.add_cog(respond(bot))  
