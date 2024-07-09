import discord
from discord.ext import commands
from discord import app_commands
import time
import json
from discord.app_commands import Choice

class messageAPI(commands.Cog):
    def __init__(self, bot):
         self.bot:commands.Bot = bot

    @app_commands.command(name="messagetrack",description="send message when message has been edited or deleted")
    @app_commands.choices(status=[
  Choice(name = "ON",value="ON"),
  Choice(name = "OFF",value="OFF"),])
    async def message(self,interaction:discord.Interaction,channel:discord.TextChannel,status:str): 
        await interaction.response.defer()
        with open('database\\data.json','r') as database:
            data = json.load(database) 
        if status == 'ON':
            if str(interaction.guild.id) in list(data["messagetrack"]["channel"]):
                data["messagetrack"]["channel"].pop(str(interaction.guild.id))
            data["messagetrack"]["channel"].update({
                interaction.guild.id:channel.id
            })

            with open('database\\data.json', 'w') as database:
                json.dump(data, database,indent=4)
            await interaction.followup.send(f"Set <#{channel.id}> to Track-message",ephemeral=True)
        else:
            if str(interaction.guild.id) in list(data["messagetrack"]["channel"]):
                if channel.id == data["messagetrack"]["channel"][str(interaction.guild.id)]:
                    data["messagetrack"]["channel"].pop(str(interaction.guild.id))

            with open('database\\data.json', 'w') as database:
                json.dump(data, database,indent=4)
            await interaction.followup.send(f"<#{channel.id}> No longer Track-message",ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_message_delete(self,payload:discord.RawMessageDeleteEvent):
        with open('database\\data.json','r') as database:
                data = json.load(database) 
        data = data["messagetrack"]["channel"]
        if not data:
            return
        if str(payload.guild_id) not in list(data):
            return
        author = 123
        channel = payload.channel_id
        content = "Unknown"
        attach = "N/A"
        if payload.cached_message:
            author = payload.cached_message.author.id
            content = payload.cached_message.content
            attach = len(payload.cached_message.attachments)
        embed=discord.Embed(description=f"Message sent by <@{author}> deleted in <#{channel}>",color=0x795ae8)
        embed.add_field(name="Content",value=f"` {content} `")
        embed.add_field(name="📫 Attachments",value=f"` {attach} `")
        if author == 123:
            author = self.bot.user
        else:
            author = payload.cached_message.author 
        embed.set_author(name=author.name+author.discriminator,icon_url=author.display_avatar.url)
        embed.set_footer(text = time.strftime("%D | %H:%M:%S"))  
        guild:discord.Guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(data[str(payload.guild_id)])
        await  channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_raw_message_edit(self,payload:discord.RawMessageUpdateEvent):
        with open('database\\data.json','r') as database:
                data = json.load(database) 
        data = data["messagetrack"]["channel"]
        if not data:
            return
        if str(payload.guild_id) not in list(data):
            return
        author = int(payload.data["author"]["id"])
        channel = payload.data["channel_id"]
        before = "Unknown"
        attach_ori = "N/A"
        if payload.cached_message:
            author = payload.cached_message.author.id
            before = payload.cached_message.content
            attach_ori = len(payload.cached_message.attachments)

        embed=discord.Embed(description=f"Message edited by <@{author}> in <#{channel}>",color=0x795ae8)
        embed.add_field(name="Orinal",value=f"` {before} `")
        embed.add_field(name="Edited",value=f"` {payload.data['content']} `",inline=True)
        embed.add_field(name="📫 Original Attachments",value=f"` {attach_ori} `",inline=False)
        embed.add_field(name="📫 Edited Attachments",value=f"` {len(payload.data['attachments'])} `",inline=True)

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(author)
        embed.set_author(name=member.name,icon_url=member.display_avatar.url)
        embed.set_footer(text = time.strftime("%D | %H:%M:%S"))  
        guild:discord.Guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(data[str(payload.guild_id)])
        await  channel.send(embed=embed)

async def setup(bot):    
  await bot.add_cog(messageAPI(bot))   