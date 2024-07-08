import discord
from discord.ext import commands
from discord import app_commands

from discord.ui import View, Button , button
class button_(View):
    @button(label="ภาคปก",style=discord.ButtonStyle.blurple,custom_id="std")
    async def standard(self,interaction:discord.Interaction,button):
        pass
    
    @button(label="ภาคเปย์",style=discord.ButtonStyle.blurple,custom_id="spe")
    async def pay(self,interaction:discord.Interaction,button):
        pass

class role(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot

    @app_commands.command(name="role",description="role selecter")
    async def role(self,interaction:discord.Interaction,message:str,standard:discord.Role,pay:discord.Role) :
        await interaction.response.defer()
        with open('database\\data.json',"w+") as database:
            data = database.read()
            print(data)
        await interaction.followup.send(view=button_())

    @commands.Cog.listener()
    async def on_interaction(self,interaction:discord.Interaction):
        if interaction.data.get('component_type') == 2:
            await interaction.response.defer()
            if interaction.data.get('custom_id') == "std":
                await interaction.followup.send(f"Give ภาคปก role to {interaction.user.name}")
            elif interaction.data.get('custom_id') == "spe":
                await interaction.followup.send(f"Give ภาคเปย์ role to {interaction.user.name}")


async def setup(bot):    
  await bot.add_cog(role(bot))  
