import PIL
from PIL import ImageFont,Image,ImageDraw
import io
import requests


from pylab import *

dic={'击杀': 1114, '助攻': 82, 'KD': 0.62, 'KPM': 0.43,
     '步战KD': 0.56, '步战KPM': 0.39, '爆头击杀': 169,
     '爆头率': '15.17%', '精准率': '9.2%', '胜场': 86,
     '败场': 72, '胜率': '54.43%', '游戏局数': 158,
     'SPM': 1258.64, '技巧值': 129.09, '总治疗量': 67,
     '昵称': 'gc_xiaozhang', '等级': 0, '游玩时间': None,
     '头像img': 'https://secure.download.dm.origin.com/production/avatar/prod/1/599/208x208.JPEG'}

#设置字体，如果没有，也可以不设置
font = ImageFont.truetype(r"C:\Windows\Fonts\simsun.ttc",40)

#打开背景图片
imageFile = "general_bg.jpg"
im1=Image.open(imageFile)

# 在图片上添加文字
draw = ImageDraw.Draw(im1)

try:
     geturl = dic.get ( '头像img' )
     geturl=requests.get(geturl)
     a = geturl.content
     aimg_bytestream = io.BytesIO ( a )
     a_imgb = Image.open ( aimg_bytestream ).resize ( (230, 230) )
except:
     a_imgb = Image.new ( "RGB", (230, 230), (255, 255, 255) )
     a_draw = ImageDraw.Draw ( a_imgb, "RGB" )
     a_draw.text ( (38, 94), "头像获取出错", font=font, fill=(0, 0, 0) )
im1.paste ( a_imgb, (100, 130) )
draw = ImageDraw.Draw ( im1, "RGB" )

draw.text((370, 130),f"{dic.get('昵称')}",(255,255,255),font=font)
draw.text((370, 220),f"{dic.get('等级')}",(255,255,255),font=font)
draw.text((370, 310),f"{dic.get('游玩时间')}",(255,255,255),font=font)

draw.text((140, 450),f"{dic.get('击杀')}",(255,255,255),font=font)
draw.text((290, 450),f"{dic.get('助攻')}",(255,255,255),font=font)
draw.text((430, 450),f"{dic.get('KD')}",(255,255,255),font=font)
draw.text((580, 450),f"{dic.get('KPM')}",(255,255,255),font=font)

draw.text((140, 590),f"{dic.get('步战KD')}",(255,255,255),font=font)
draw.text((290, 590),f"{dic.get('步战KPM')}",(255,255,255),font=font)
draw.text((430, 590),f"{dic.get('爆头击杀')}",(255,255,255),font=font)
draw.text((580, 590),f"{dic.get('爆头率')}",(255,255,255),font=font)

draw.text((140, 730),f"{dic.get('精准率')}",(255,255,255),font=font)
draw.text((290, 730),f"{dic.get('胜场')}",(255,255,255),font=font)
draw.text((430, 730),f"{dic.get('败场')}",(255,255,255),font=font)
draw.text((580, 730),f"{dic.get('胜率')}",(255,255,255),font=font)

draw.text((140, 870),f"{dic.get('游戏局数')}",(255,255,255),font=font)
draw.text((280, 870),f"{dic.get('SPM')}",(255,255,255),font=font)
draw.text((430, 870),f"{dic.get('技巧值')}",(255,255,255),font=font)
draw.text((580, 870),f"{dic.get('总医疗量')}",(255,255,255),font=font)

plt.imshow(im1)
plt.show()
im1.save("custom.png")
print(dic['击杀'])
