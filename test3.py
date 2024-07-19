from textwrap3 import wrap
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import PIL
black = (0,0,0)
font_path = r"utility\absent\THSarabunNew.ttf"
def check_lenght(word,startpoint,endpoint):
    font = ImageFont.truetype(font_path, 35)
    right = startpoint + font.getlength(word)
    i = 40
    while right > endpoint:
        font = ImageFont.truetype(font_path, i)
        i-=1
        right = startpoint + font.getlength(word)
    return font

form = Image.open(r"utility\absent\absentform_demo.jpg")
draw = ImageDraw.Draw(form)
font = ImageFont.truetype(font_path, 35)
draw.text((645, 485),"19",black,font=font,anchor="mm")
draw.text((850, 485),"สิงหาคม",black,font=font,anchor="mm")
draw.text((1080, 485),"2567",black,font=font,anchor="mm")

draw.text((200, 600),"อ. วรพล ก้อนนาค",black,font=font)
draw.text((580, 690),"นาย ธนัต เทพโพธา",black,font=font)
draw.text((270, 740),"6710405389",black,font=font)
draw.text((580, 740),"1",black,font=font)
draw.text((730, 740),"วิทยาการคอมพิวเตอร์",black,font=font)
draw.text((240, 785),"วิทยาศาสตร์",black,font=font)
address = "xxx ซอย พหลโยธิน xx แยก xx แขวงอนุสาวรีย์ xxxx xxxxxxxxx xxxx"
font_s = check_lenght(address,100,700)
draw.text((410, 855),address,black,font=font_s,anchor="mm")
draw.text((810, 830),"0952475183",black,font=font)

mesage = wrap('\tเนื่องด้วยกระผมมีเหตุธุระด่วนจำเป็นโดยเป็นการที่แพทย์นัดพบอย่างกระทันหันเพื่อติดตามการรักษา และวินิจฉัยการรักษาโรคต่อเนื่องทำให้กระผมไม่สามารถเข้าเรียนได้ตามปกติจึงเรียนมาเพื่อพิจารณาอนุญาต',100)
offet = 970
for line in mesage:
    draw.text((110, offet),line,black,font=font)
    offet += 45

signature = Image.open(r"database\signature\6710405389.png")
if signature.mode == 'RGBA':
    alpha = signature.split()[3]
    bgmask = alpha.point(lambda x: 255-x)
    signature = signature.convert('RGB')
    signature.paste((255,255,255), None, bgmask)

width = 150
signature = signature.resize((width,int((width / signature.size[0]) * signature.size[1])),Image.LANCZOS)
signature = signature.convert('RGBA')

form.paste(signature, (750,1300))
draw.text((750, 1385),"ธนัต เทพโพธา",black,font=font)    

  
form.save("final.jpg")