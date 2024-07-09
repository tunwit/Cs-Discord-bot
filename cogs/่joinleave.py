import discord
from discord.ext import commands
from discord import app_commands
import json
from discord.app_commands import Choice
from typing import List
from datetime import datetime

class joinleaveAPI(commands.Cog):
    def __init__(self, bot):
         self.bot:commands.Bot = bot
         self.invites = self.bot.invites

    def get_invite(self,lst,code):
        invites = lst
        for i in invites:
            if i.code == code:
                return i
        return None

    @commands.Cog.listener()
    async def on_member_join(self,member:discord.Member):
        with open('database\\data.json','r') as database:
                data = json.load(database) 
        data = data["joinleave"]["channel"]
        if not data:
            return
        if str(member.guild.id) not in list(data):
            return
        
        before = self.invites[str(member.guild.id)]
        after = await member.guild.invites()
        invite = None
        for event in before:
            if event.uses < self.get_invite(after,event.code).uses:
                invite = event
        embed=discord.Embed(title=f"{member.name} Join the server",color=0x19AD3B)
        embed.add_field(name="Tag",value=f"<@{member.id}>")
        embed.add_field(name="Join Date",value=f'` {datetime.now().strftime("%d/%m/%y | %H:%M:%S")} `',inline=True)
        embed.add_field(name="Id",value=f'` {member.id} `',inline=False)
        embed.add_field(name="Account Creation",value=f'` {member.created_at.strftime("%d/%m/%y")} `',inline=False)
        
        if invite:
            embed.add_field(name="Inviter",value=f"<@{invite.inviter.id}>",inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=member.guild.name,icon_url=member.guild.icon.url)

        guild:discord.Guild = self.bot.get_guild(member.guild.id)
        channel = guild.get_channel(data[str(member.guild.id)])
        await  channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self,member:discord.Member):   
        with open('database\\data.json','r') as database:
                data = json.load(database) 
        data = data["joinleave"]["channel"]
        if not data:
            return
        if str(member.guild.id) not in list(data):
            return

        embed=discord.Embed(title=f"{member.name} Leave the server",color=0xcc8c2d)
        embed.add_field(name="Tag",value=f"<@{member.id}>")
        embed.add_field(name="Id",value=f'` {member.id} `',inline=True)
        embed.add_field(name="Join Date",value=f'` {member.joined_at.strftime("%d/%m/%y | %H:%M:%S")} `',inline=False)
        embed.add_field(name="Leave Date",value=f'` {datetime.now().strftime("%d/%m/%y | %H:%M:%S")} `',inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=member.guild.name,icon_url=member.guild.icon.url)

        guild:discord.Guild = self.bot.get_guild(member.guild.id)
        channel = guild.get_channel(data[str(member.guild.id)])
        await  channel.send(embed=embed)
        

    @app_commands.command(name="joinleave",description="send message when user join or leave server")
    @app_commands.choices(status=[
  Choice(name = "ON",value="ON"),
  Choice(name = "OFF",value="OFF"),])
    async def joinleave(self,interaction:discord.Interaction,channel:discord.TextChannel,status:str): 
        await interaction.response.defer()
        with open('database\\data.json','r') as database:
            data = json.load(database) 
        if status == 'ON':
            if str(interaction.guild.id) in list(data["joinleave"]["channel"]):
                data["joinleave"]["channel"].pop(str(interaction.guild.id))
            data["joinleave"]["channel"].update({
                interaction.guild.id:channel.id
            })

            with open('database\\data.json', 'w') as database:
                json.dump(data, database,indent=4)
            await interaction.followup.send(f"Set <#{channel.id}> to notify join/leave",ephemeral=True)
        else:
            if str(interaction.guild.id) in list(data["joinleave"]["channel"]):
                if channel.id == data["joinleave"]["channel"][str(interaction.guild.id)]:
                    data["joinleave"]["channel"].pop(str(interaction.guild.id))

            with open('database\\data.json', 'w') as database:
                json.dump(data, database,indent=4)
            await interaction.followup.send(f"<#{channel.id}> No longer notify join/leave",ephemeral=True)


async def setup(bot):    
  await bot.add_cog(joinleaveAPI(bot))   