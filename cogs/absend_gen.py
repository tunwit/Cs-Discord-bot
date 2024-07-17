import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
import json
import os
from discord.utils import MISSING

class registermodal(ui.Modal):
    name = ui.TextInput(label='ชื่อจริง',required=True)
    branch = ui.TextInput(label='สาขาวิชา', style=discord.TextStyle.short,required=True)
    faculty = ui.TextInput(label='คณะ', style=discord.TextStyle.short,required=True)
    address = ui.TextInput(label='ที่อยู่',required=True)
    phone = ui.TextInput(label='โทรศัพท์',required=True)

    def __init__(self, nisit_id) -> None:
        self.nisit_id = nisit_id
        super().__init__(title='Absend generator Registration')

    async def on_submit(self, interaction: discord.Interaction):
        with open('database\\data.json','r') as database:
            data = json.load(database) 
        data["absend_gen"].update({
            self.nisit_id:{
                "name":self.name.value,
                "branch":self.branch.value,
                "faculty":self.faculty.value,
                "address":self.address.value, 
                "phone":self.phone.value
            }
        })
        with open('database\\data.json', 'w') as database:
                json.dump(data, database,indent=4)

        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)

class absendform(ui.Modal):
    professsor = ui.TextInput(label='อาจารย์',required=True)
    message = ui.TextInput(label='ข้อความ', style=discord.TextStyle.paragraph,required=True)

    def __init__(self, nisit_id) -> None:
        self.nisit_id = nisit_id
        super().__init__(title='Absend Form')

    async def on_submit(self, interaction: discord.Interaction):
        with open('database\\data.json','r') as database:
            data = json.load(database) 
        
        if not os.path.exists(f'database/signature/{self.nisit_id}.png'):
            await interaction.response.send_message(f"Don't have your signature uploaded please Upload your signature using `/upload_signature`", ephemeral=True)
            return
        await interaction.response.send_message(f' {data["absend_gen"][str(self.nisit_id)]}!', ephemeral=True)

class absendAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot

    @app_commands.command(name="absend_generator",description="Generate absend form")
    async def absend(self,interaction:discord.Interaction,nisit_id:int):
        with open('database\\data.json','r') as database:
            data = json.load(database) 
        if str(nisit_id) in list(data["absend_gen"]):
            modal = absendform(nisit_id = nisit_id)
            await interaction.response.send_modal(modal)
        else:
            modal = registermodal(nisit_id = nisit_id)
            await interaction.response.send_modal(modal)


    @app_commands.command(name="upload_signature",description="Upload your Signature to use")
    async def upload_signature(self,interaction:discord.Interaction,nisit_id:int,file:discord.Attachment):
        await interaction.response.send_message("Now implemented",ephemeral=True)


async def setup(bot):    
  await bot.add_cog(absendAPI(bot))  
