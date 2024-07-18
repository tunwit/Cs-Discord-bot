from textwrap3 import wrap
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import PIL
def check_lenght(word,startpoint,endpoint):
    font = ImageFont.truetype(r"utility\absent\cordia_0.ttf", 35)
    right = startpoint + font.getlength(word)
    i = 40
    while right > endpoint:
        font = ImageFont.truetype(r"utility\absent\cordia_0.ttf", i)
        i-=1
        right = startpoint + font.getlength(word)
    return font

form = Image.open(r"utility\absent\absentform.jpg")
draw = ImageDraw.Draw(form)
font = ImageFont.truetype(r"utility\absent\cordia_0.ttf", 35)
draw.text((200, 595),"อ. วรพล ก้อนนาค",(30, 52, 84),font=font)
draw.text((580, 690),"นาย ธนัต เทพโพธา",(30, 52, 84),font=font)
draw.text((270, 735),"6710405389",(30, 52, 84),font=font)
draw.text((580, 735),"1",(30, 52, 84),font=font)
draw.text((730, 735),"วิทยาการคอมพิวเตอร์",(30, 52, 84),font=font)
draw.text((240, 780),"วิทยาศาสตร์",(30, 52, 84),font=font)
address = "149 ซอย พหลโยธิน 53 แยก 11 แขวงอนุสาวรีย์ เขตบางเขน กรุงเทพมหานคร 10220"
font_s = check_lenght(address,100,700)
draw.text((410, 855),address,(30, 52, 84),font=font_s,anchor="mm")
draw.text((810, 825),"0952475183",(30, 52, 84),font=font)

mesage = wrap('\tเนื่องด้วยกระผมมีเหตุธุระด่วนจำเป็นโดยเป็นการที่แพทย์นัดพบอย่างกระทันหันเพื่อติดตามการรักษา และวินิจฉัยการรักษาโรคต่อเนื่องทำให้กระผมไม่สามารถเข้าเรียนได้ตามปกติจึงเรียนมาเพื่อพิจารณาอนุญาต',100)
offet = 965
for line in mesage:
    draw.text((110, offet),line,(30, 52, 84),font=font)
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
draw.text((750, 1385),"ธนัต เทพโพธา",(0, 0, 0),font=font)    
form.show()