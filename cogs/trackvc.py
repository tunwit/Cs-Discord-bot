import discord
from discord.ext import commands
from discord import app_commands
import time
import json
from discord.app_commands import Choice

class trackAPI(commands.Cog):
    def __init__(self, bot):
         self.bot = bot

    @app_commands.command(name="trackvc",description="send message when member join or leave vc")
    @app_commands.choices(status=[
  Choice(name = "ON",value="ON"),
  Choice(name = "OFF",value="OFF"),])
    async def track(self,interaction:discord.Interaction,channel:discord.TextChannel,status:str): 
        await interaction.response.defer()
        with open('database\\data.json','r') as database:
            data = json.load(database) 
        if status == 'ON':
            if str(interaction.guild.id) in list(data["trackvc"]["channel"]):
                data["trackvc"]["channel"].pop(str(interaction.guild.id))
            data["trackvc"]["channel"].update({
                interaction.guild.id:channel.id
            })

            with open('database\\data.json', 'w') as database:
                json.dump(data, database,indent=4)
            await interaction.followup.send(f"Set <#{channel.id}> to Track-vc",ephemeral=True)
        else:
            if str(interaction.guild.id) in list(data["trackvc"]["channel"]):
                if channel.id == data["trackvc"]["channel"][str(interaction.guild.id)]:
                    data["trackvc"]["channel"].pop(str(interaction.guild.id))

            with open('database\\data.json', 'w') as database:
                json.dump(data, database,indent=4)
            await interaction.followup.send(f"<#{channel.id}> No longer Track-vc",ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member:discord.Member, before, after): 
        with open('database\\data.json','r') as database:
                data = json.load(database) 
        data = data["trackvc"]["channel"]
        if not data:
            return
        if member == self.bot.user:
           return
        if str(member.guild.id) not in list(data):
            return
        if before.channel == None and after.channel != None: #None -> join
            embed=discord.Embed(description=f"✅ **<@{member.id}>** Joined 🔊 <#{after.channel.id}>",color=0x19AD3B)
        elif before.channel != None and after.channel == None: #Join -> None
            embed=discord.Embed(description=f"📴 **<@{member.id}>** Leave 🔊 <#{before.channel.id}>",color=0xcc8c2d)
        elif before.channel != None and after.channel != None and before.channel != after.channel: #Join -> Join (move to)
            embed=discord.Embed(description=f"🔃 **<@{member.id}>** Move from 🔊 <#{before.channel.id}> to 🔊 <#{after.channel.id}>",color=0x2bc2b3)
        else:
            return
        embed.set_author(name=member.name,icon_url=member.display_avatar.url)
        embed.set_footer(text = time.strftime("%D | %H:%M:%S"))  
        channel = member.guild.get_channel(data[str(member.guild.id)])
        await channel.send(embed=embed)

async def setup(bot):    
  await bot.add_cog(trackAPI(bot))   