import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
import json
import os
from utility.get_signature import crop_text_from_image

class registermodal(ui.Modal):
    name = ui.TextInput(label='ชื่อจริง',required=True)
    branch = ui.TextInput(label='สาขาวิชา', style=discord.TextStyle.short,required=True)
    faculty = ui.TextInput(label='คณะ', style=discord.TextStyle.short,required=True)
    address = ui.TextInput(label='ที่อยู่',required=True)
    phone = ui.TextInput(label='โทรศัพท์',required=True)

    def __init__(self, nisit_id,file) -> None:
        self.nisit_id = nisit_id
        self.file = file
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
        with open('database\\data.json', 'w',encoding='utf8') as database:
                json.dump(data, database,indent=4,ensure_ascii=False)

        image = crop_text_from_image(await self.file.read())
        image.save(f"database/signature/{self.nisit_id}.png", format="PNG")
        await interaction.response.send_message(f'Thanks for your registration, {interaction.user.name}!', ephemeral=True)

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
        if str(nisit_id) not in list(data["absend_gen"]):
            await interaction.response.send_message("You are not registed use `/absend_register`",ephemeral=True)
            return
        modal = absendform(nisit_id = nisit_id)
        await interaction.response.send_modal(modal)


    @app_commands.command(name="absend_register",description="Register your personal infomation")
    @app_commands.describe(signature="Your signature sign file written in white background")
    async def absend_register(self,interaction:discord.Interaction,nisit_id:int,signature:discord.Attachment):
        modal = registermodal(nisit_id = nisit_id,file=signature)
        await interaction.response.send_modal(modal)

async def setup(bot):    
  await bot.add_cog(absendAPI(bot))  