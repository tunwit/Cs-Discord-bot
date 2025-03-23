import discord
from discord.ext import commands
from discord import app_commands

class autoroleAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member:discord.Member):
        database = self.bot.cs_mango["autorole"]
        data = database.find_one({"guild_id":str(member.guild.id)})
        if member == self.bot.user:
            return
        if member.bot:
            return
        if not data:
            return
        target_role = member.guild.get_role(data['role_id'])
        await member.add_roles(target_role,atomic=True)
    

    @app_commands.command(name="autorole",description="auto role setup")
    async def autorole(self,interaction:discord.Interaction,role:discord.Role):
        database = self.bot.cs_mango["trackvc"]
        data = database.find_one({"guild_id":str(interaction.guild.id)})
        if not data:  
            database.insert_one({
            "guild_id":str(interaction.guild.id),
            "role_id":str(role.id)
            })  
            await interaction.response.send_message(f"Giving role`{role.name}` to everyone that join server",ephemeral=True)
        else:
            database.delete_one({"guild_id":str(interaction.guild.id)})          
            await interaction.response.send_message(f"`autorole `{role.name}` Cancled",ephemeral=True)

async def setup(bot):    
  await bot.add_cog(autoroleAPI(bot))   
