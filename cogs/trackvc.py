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
        if status == 'ON':
            with open('database\\data.json','r') as database:
                data = json.load(database) 
                data["trackvc"]["channel"].update({
                    interaction.guild.id:channel.id
                })

            with open('database\\data.json', 'w') as database:
                json.dump(data, database,indent=4)
            await interaction.followup.send(f"Set <#{channel.id}> to Track-vc",ephemeral=True)
        else:
            with open('database\\data.json','r') as database:
                data = json.load(database) 
                if channel.id in data["trackvc"]["channel"]:
                    data["trackvc"]["channel"].pop(interaction.guild.id)

            with open('database\\data.json', 'w') as database:
                json.dump(data, database,indent=4)
            await interaction.followup.send(f"<#{channel.id}> No longer Track-vc",ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member:discord.Member, before, after): 
        with open('database\\data.json','r') as database:
                data = json.load(database) 
        data = data["trackvc"]["channel"]
        print(member.guild.id,data)
        if not data:
            return
        if member == self.bot.user:
           return
        if str(member.guild.id) not in list(data):
            return
        if before.channel == None and after.channel != None: #None -> join
            embed=discord.Embed(description=f"✅ **{member}** เข้าร่วมช่อง ``🔊 {after.channel.name}``",color=0x19AD3B)
        elif before.channel != None and after.channel == None: #Join -> None
            embed=discord.Embed(description=f"📴 **{member}** ออกจากช่อง ``🔊 {before.channel.name}``",color=0xcc8c2d)
        elif before.channel != None and after.channel != None and before.channel != after.channel: #Join -> Join (move to)
            embed=discord.Embed(description=f"🔃 **{member}** ย้ายจาก ``🔊 {before.channel.name}`` ไปที่ ``🔊 {after.channel.name}``",color=0x2bc2b3)
        else:
            return
        embed.set_author(name=member.name+member.discriminator,icon_url=member.display_avatar.url)
        embed.set_footer(text = time.strftime("%D | %H:%M:%S"))  
        channel = member.guild.get_channel(data[str(member.guild.id)])
        await channel.send(embed=embed)

async def setup(bot):    
  await bot.add_cog(trackAPI(bot))   