import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
import json
import os
from utility.get_signature import crop_text_from_image
from textwrap3 import wrap
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import PIL
from datetime import datetime
import io

font_path = r"utility\absent\THSarabunNew.ttf"
month = {
    1:"มกราคม",
    2:"กุมภาพันธ์",
    3:"มีนาคม",
    4:"เมษายน",
    5:"พฤษภาคม",
    6:"มิถุนายน",
    7:"กรกฎาคม",
    8:"สิงหาคม",
    9:"กันยายน",
    10:"ตุลาคม",
    11:"พฤศจิกายน",
    12:"ธันวาคม",
}
def check_lenght(word,startpoint,endpoint):
        font = ImageFont.truetype(font_path, 35)
        right = startpoint + font.getlength(word)
        i = 40
        while right > endpoint:
            font = ImageFont.truetype(font_path, i)
            i-=1
            right = startpoint + font.getlength(word)
        return font

def create_form(nisit_data:dict):
    black = (0,0,0)
    form = Image.open(r"utility\absent\absentform_demo.jpg")
    draw = ImageDraw.Draw(form)
    font = ImageFont.truetype(font_path, 35)
    date = datetime.now()
    draw.text((645, 485),str(date.day),black,font=font,anchor="mm")
    draw.text((850, 485),month[date.month],black,font=font,anchor="mm")
    draw.text((1080, 485),str(date.year+543),black,font=font,anchor="mm")

    draw.text((200, 600),nisit_data["professsor"],black,font=font)
    draw.text((580, 690),nisit_data["nisit"]["name"],black,font=font)
    draw.text((270, 740),nisit_data["nisit_id"],black,font=font)
    draw.text((580, 740),"1",black,font=font)
    draw.text((730, 740),nisit_data["nisit"]["faculty"],black,font=font)
    draw.text((240, 785),nisit_data["nisit"]["branch"],black,font=font)
    address = nisit_data["nisit"]["address"]
    font_s = check_lenght(address,100,700)
    draw.text((410, 855),address,black,font=font_s,anchor="mm")
    draw.text((810, 830),nisit_data["nisit"]["phone"],black,font=font)

    mesage = wrap(f'\t{nisit_data["message"]}',100)
    offet = 970
    for line in mesage:
        draw.text((110, offet),line,black,font=font)
        offet += 45

    signature = Image.open(f"database\\signature\\{nisit_data['nisit_id']}.png")
    if signature.mode == 'RGBA':
        alpha = signature.split()[3]
        bgmask = alpha.point(lambda x: 255-x)
        signature = signature.convert('RGB')
        signature.paste((255,255,255), None, bgmask)

    width = 150
    signature = signature.resize((width,int((width / signature.size[0]) * signature.size[1])),Image.LANCZOS)
    signature = signature.convert('RGBA')

    form.paste(signature, (750,1300))
    draw.text((750, 1385),nisit_data["nisit"]["name"],black,font=font)    
    return form

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
        
        data = {
            "nisit":data["absend_gen"][str(self.nisit_id)],
            "nisit_id":str(self.nisit_id),
            "professsor":self.professsor.value,
            "message":self.message.value
        }
        form = create_form(data)
        with io.BytesIO() as byte:
            form.save(byte,format="PNG")
            byte.seek(0)
            await interaction.response.send_message("Succesfully send you an absent form `see in your DM.`",ephemeral=True)
            await interaction.user.send(file=discord.File(byte,filename=str(self.nisit_id)+".png"))

class absendAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot

    @app_commands.command(name="absend_generator",description="Generate absend form")
    async def absend(self,interaction:discord.Interaction,nisit_id:int):
        with open('database\\data.json','r') as database:
            data = json.load(database) 
        if str(nisit_id) not in list(data["absend_gen"]):
            await interaction.response.send_message("You are not registered use `/absend_register`",ephemeral=True)
            return
        modal = absendform(nisit_id = nisit_id)
        await interaction.response.send_modal(modal)


    @app_commands.command(name="absend_register",description="Register your personal infomation")
    @app_commands.describe(signature="Your signature sign file written in white background")
    async def absend_register(self,interaction:discord.Interaction,nisit_id:int,signature:discord.Attachment):
        modal = registermodal(nisit_id = nisit_id,file=signature)
        with open('database\\data.json','r') as database:
            data = json.load(database) 
        if str(nisit_id) in list(data["absend_gen"]):
            await interaction.response.send_message("You are already registered if you want to edit please contact developer",ephemeral=True)
            return
        await interaction.response.send_modal(modal)

async def setup(bot):    
  await bot.add_cog(absendAPI(bot))  
