import discord
from discord.ext import commands
from discord import app_commands
import json
from discord.errors import Forbidden
from discord.ui import View , button

class button_(View):
    @button(label="ภาคปก",style=discord.ButtonStyle.blurple,custom_id="std_cslover_role_id")
    async def standard(self,interaction:discord.Interaction,button):
        pass
    
    @button(label="ภาคเปย์",style=discord.ButtonStyle.blurple,custom_id="spe_cslover_role_id")
    async def pay(self,interaction:discord.Interaction,button):
        pass

class role(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot

    @app_commands.command(name="role",description="role selecter")
    async def role(self,interaction:discord.Interaction,message:str,standard:discord.Role,pay:discord.Role) :
        await interaction.response.defer()
        database = self.bot.cs_mango["role"]
        data = database.find_one({"name":"roleconfig"})
        if not data:
            database.insert_one({
                "name":"roleconfig",
                "std_cslover_role_id":standard.id,
                "spe_cslover_role_id":pay.id
            })
        else:
            database.update_one(data,{ "$set": {
                "name":"roleconfig",
                "std_cslover_role_id":standard.id,
                "spe_cslover_role_id":pay.id
            }})

        await interaction.followup.send(message,view=button_())

    @commands.Cog.listener()
    async def on_interaction(self,interaction:discord.Interaction):
        if interaction.data.get('component_type') == 2: #check is button
            custom_id = interaction.data.get('custom_id')
            if "_cslover_role_id" in custom_id:#check is pressed from role selector
                await interaction.response.defer()
                database = self.bot.cs_mango["role"]
                data = database.find_one({"name":"roleconfig"})
                target_role = interaction.guild.get_role(data[custom_id])
                if not interaction.user.get_role(data[custom_id]):
                    try:
                        await interaction.user.add_roles(target_role,atomic=True)
                        embed = discord.Embed(description=f"Give <@&{target_role.id}> to {interaction.user.name}",
                            color=0x55cf51)
                    except Forbidden:
                        embed = discord.Embed(title="Missing Permission",
                            description=f"⛔️ This bot don't have permission to add <@&{target_role.id}>. Make sure to prioritize Role of this bot.\n\n If issue still exists please contact developer to solving issue \n` Discord : littlxbirdd `",
                            color=0xff4133)
                else:
                    await interaction.user.remove_roles(target_role)
                    embed = discord.Embed(description=f"Remove <@&{target_role.id}> from {interaction.user.name}",
                            color=0xe8c25a)
                    
                await interaction.followup.send(embed=embed,ephemeral=True)
                    

async def setup(bot):    
  await bot.add_cog(role(bot))  
