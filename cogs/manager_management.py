import discord
from discord.ext import commands
from discord import app_commands,File
from discord.app_commands import Choice
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import json
from typing import Optional
from utility.check_is_manager import is_manager
class managerAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot

    @app_commands.command(name="manager",description="manager management")
    @app_commands.choices(
        method=[
            Choice(name="Add", value=1),
            Choice(name="Remove", value=0)
        ]
    )
    @app_commands.check(is_manager)
    async def manager(self,interaction:discord.Interaction,user:discord.User,method:int):
        await interaction.response.defer()
        with open('database\\data.json','r') as database:
            data = json.load(database)
        if method:
            data["manager"].append(user.id)
            await interaction.followup.send(f"`{user.id}` is Added")
        else:
            data["manager"].remove(user.id)
            await interaction.followup.send(f"`{user.id}` is Removed")
        with open('database\\data.json', 'w') as database:
            json.dump(data, database,indent=4)
    

    @app_commands.command(name="manager_id",description="manager management by id")
    @app_commands.choices(
        method=[
            Choice(name="Add", value=1),
            Choice(name="Remove", value=0)
        ]
    )
    @app_commands.check(is_manager)
    async def manager_id(self,interaction:discord.Interaction,user_id:int,method:int):
        await interaction.response.defer()
        with open('database\\data.json','r') as database:
            data:list = json.load(database)
        if method:
            data["manager"].append(user_id)
            await interaction.followup.send(f"`{user_id}` is Removed")
        else:
            data["manager"].remove(user_id)
            await interaction.followup.send(f"`{user_id}` is Removed")
        with open('database\\data.json', 'w') as database:
            json.dump(data, database,indent=4)

        

async def setup(bot):    
  await bot.add_cog(managerAPI(bot))  
