import discord
from discord.ext import commands
from discord import app_commands
import time
from discord.app_commands import Choice

class messageAPI(commands.Cog):
    def __init__(self, bot):
         self.bot:commands.Bot = bot

    @app_commands.command(name="messagetrack",description="send message when message has been edited or deleted")
    @app_commands.choices(status=[
  Choice(name = "ON",value="ON"),
  Choice(name = "OFF",value="OFF"),])
    async def message(self,interaction:discord.Interaction,channel:discord.TextChannel,status:str): 
        database = self.bot.cs_mango["messagetrack"]
        data = database.find_one({"guild_id":str(interaction.guild.id)})
        if status == 'ON':
            if not data:  
                database.insert_one({
                "guild_id":str(interaction.guild.id),
                "text_channel":str(channel.id)
                })                            
            await interaction.response.send_message(f"Set <#{channel.id}> to Track-message",ephemeral=True)
        else:
            if data:
                database.delete_one({"guild_id":str(interaction.guild.id)})
            else:
                await interaction.response.send_message(f"<#{channel.id}> Is not on the list",ephemeral=True)
                return
            await interaction.response.send_message(f"<#{channel.id}> No longer Track-message",ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_message_delete(self,payload:discord.RawMessageDeleteEvent):
        database = self.bot.cs_mango["messagetrack"]
        data = database.find_one({"guild_id":str(payload.guild_id)})
        if not data:
            return
        author = 123
        if payload.cached_message:
            user = payload.cached_message.author
            if user.bot:
                return
        channel = payload.channel_id
        content = "Unknown"
        attach = "N/A"
        author = "Unknown"
        if payload.cached_message:
            content = payload.cached_message.content
            attach = len(payload.cached_message.attachments)
            author = payload.cached_message.author.id
        try:
            embed=discord.Embed(description=f"Message sent by <@{author}> deleted in <#{channel}>",color=0x795ae8)
            embed.add_field(name="Content",value=f"` {content} `")
            embed.add_field(name="📫 Attachments",value=f"` {attach} `")
            embed.set_footer(text = time.strftime("%D | %H:%M:%S"))  
            guild:discord.Guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(int(data["text_channel"]))
            await  channel.send(embed=embed)
        except Exception as e:
            print(e)
    
    
    @commands.Cog.listener()
    async def on_raw_message_edit(self,payload:discord.RawMessageUpdateEvent):
        database = self.bot.cs_mango["messagetrack"]
        data = database.find_one({"guild_id":str(payload.guild_id)})
        if not data:
            return
        if payload.cached_message:
            user = payload.cached_message.author
            if user.bot:
                return
        channel = payload.data["channel_id"]
        before = "Unknown"
        attach_ori = "N/A"
        author = 123
        if payload.cached_message:
            author = payload.cached_message.author.id
            before = payload.cached_message.content
            attach_ori = len(payload.cached_message.attachments)
        
        try:
            embed=discord.Embed(description=f"Message edited by <@{author}> in <#{channel}>",color=0x795ae8)
            embed.add_field(name="Orinal",value=f"` {before} `")
            embed.add_field(name="Edited",value=f"` {payload.data['content']} `",inline=True)
            embed.add_field(name="📫 Original Attachments",value=f"` {attach_ori} `",inline=False)
            embed.add_field(name="📫 Edited Attachments",value=f"` {len(payload.data['attachments'])} `",inline=True)
            guild = self.bot.get_guild(payload.guild_id)
            embed.set_footer(text = time.strftime("%D | %H:%M:%S"))  
            guild:discord.Guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(int(data["text_channel"]))
            await  channel.send(embed=embed)
        except Exception as e:
            print(e)


async def setup(bot):    
  await bot.add_cog(messageAPI(bot))   