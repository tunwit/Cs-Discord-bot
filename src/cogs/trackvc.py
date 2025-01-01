import discord
from discord.ext import commands
from discord import app_commands
import time
from discord.app_commands import Choice

class trackAPI(commands.Cog):
    def __init__(self, bot):
         self.bot = bot

    @app_commands.command(name="trackvc",description="send message when member join or leave vc")
    @app_commands.choices(status=[
  Choice(name = "ON",value="ON"),
  Choice(name = "OFF",value="OFF"),])
    async def track(self,interaction:discord.Interaction,channel:discord.TextChannel,status:str): 
        database = self.bot.cs_mango["trackvc"]
        data = database.find_one({"guild_id":str(interaction.guild.id)})
        if status == 'ON':
            if not data:  
                database.insert_one({
                "guild_id":str(interaction.guild.id),
                "text_channel":str(channel.id)
                })                            
            await interaction.response.send_message(f"Set <#{channel.id}> to Track-vc",ephemeral=True)
        else:
            if data:
                database.delete_one({"guild_id":str(interaction.guild.id)})
            else:
                await interaction.response.send_message(f"<#{channel.id}> Is not on the list",ephemeral=True)
                return
            await interaction.response.send_message(f"<#{channel.id}> No longer Track-vc",ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member:discord.Member, before:discord.VoiceState, after:discord.VoiceState): 
        database = self.bot.cs_mango["trackvc"]
        data = database.find_one({"guild_id":str(member.guild.id)})
        if not data:
            return
        if member == self.bot.user:
           return
        if before.channel == None and after.channel != None: #None -> join
            embed=discord.Embed(description=f"<a:check:1259893528499195954> | **`{member.display_name}`** Joined 🔊 `{after.channel.name}`",color=0x19AD3B)
        elif before.channel != None and after.channel == None: #Join -> None
            embed=discord.Embed(description=f"<a:w_check:1259893785207509052> | **`{member.display_name}`** Leave 🔊 `{before.channel.name}`",color=0xcc8c2d)
        elif before.channel != None and after.channel != None and before.channel != after.channel: #Join -> Join (move to)
            embed=discord.Embed(description=f"🔃 **`{member.display_name}`** Move from 🔊 `{before.channel.name}` to 🔊 `{after.channel.name}`",color=0x2bc2b3)
        else:
            return
        embed.set_author(name=member.name,icon_url=member.display_avatar.url)
        embed.set_footer(text = time.strftime("%D | %H:%M:%S"))  
        channel = member.guild.get_channel(int(data["text_channel"]))
        await channel.send(embed=embed)

async def setup(bot):    
  await bot.add_cog(trackAPI(bot))   