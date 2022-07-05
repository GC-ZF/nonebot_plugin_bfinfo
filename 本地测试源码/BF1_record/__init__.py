from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import  Bot, PrivateMessageEvent,GroupMessageEvent,Message
import json
import io, os
from PIL import ImageFont, Image, ImageDraw
import requests
from pylab import *
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment

BFIS = on_command("BFI", block=True, priority=12)
BFVS = on_command("BFV", block=True, priority=12)

get_json = ""


# 转换秒数为时分秒的形式
def seconds_trans(seconds):
    m, s = divmod ( seconds, 60 )
    h, m = divmod ( m, 60 )
    return "%02d时%02d分%02d秒" % (h, m, s)

def get_data(name):
    game_name = name
    global get_json
    url = f'https://api.gametools.network/bf1/all/?name={game_name}&lang=en-us'
    get_data = requests.get ( url )
    get_json = json.loads ( get_data.text )

def get_dataV(name):
    game_name = name
    global get_json
    url = f'https://api.gametools.network/bfv/all/?name={game_name}&lang=en-us'
    get_data = requests.get ( url )
    get_json = json.loads ( get_data.text )
    
# 对数据处理为字典
def general():
    general_dict = {}
    general_dict[ '击杀' ] = get_json[ 'kills' ]
    general_dict[ '助攻' ] = int ( get_json[ 'killAssists' ] )
    general_dict[ 'KD' ] = get_json[ 'killDeath' ]
    general_dict[ 'KPM' ] = get_json[ 'killsPerMinute' ]
    general_dict[ '步战KD' ] = get_json[ 'infantryKillDeath' ]
    general_dict[ '步战KPM' ] = get_json[ 'infantryKillsPerMinute' ]
    general_dict[ '爆头击杀' ] = get_json[ 'headShots' ]
    general_dict[ '爆头率' ] = get_json[ 'headshots' ]
    general_dict[ '精准率' ] = get_json[ 'accuracy' ]
    general_dict[ '胜场' ] = get_json[ 'wins' ]
    general_dict[ '败场' ] = get_json[ 'loses' ]
    general_dict[ '胜率' ] = get_json[ 'winPercent' ]
    general_dict[ '游戏局数' ] = get_json[ 'roundsPlayed' ]
    general_dict[ 'SPM' ] = get_json[ 'scorePerMinute' ]
    general_dict[ '技巧值' ] = get_json[ 'skill' ]
    general_dict[ '总治疗量' ] = int ( get_json[ 'heals' ] )
    general_dict[ '昵称' ] = get_json[ 'userName' ]
    general_dict[ '等级' ] = get_json[ 'rank' ]
    general_dict[ '游玩时间' ] = seconds_trans ( get_json[ 'secondsPlayed' ] )
    general_dict[ '头像img' ] = get_json[ 'avatar' ]

    return general_dict


# 绘制图像
def draw_img():
    dic = general ()
    # 设置字体，如果没有，也可以不设置
    font = ImageFont.truetype ( r"/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc", 40 )

    # 打开背景图片
    imageFile = "src/plugins/BF1_record/general_bg.jpg"
    im1 = Image.open ( f"{imageFile}" )

    # 在图片上添加文字
    draw = ImageDraw.Draw ( im1 )

    try:
        geturl = dic.get ( '头像img' )
        geturl = requests.get ( geturl )
        a = geturl.content
        aimg_bytestream = io.BytesIO ( a )
        a_imgb = Image.open ( aimg_bytestream ).resize ( (230, 230) )
    except:
        a_imgb = Image.new ( "RGB", (230, 230), (255, 255, 255) )
        a_draw = ImageDraw.Draw ( a_imgb, "RGB" )
        a_draw.text ( (38, 94), "头像获取出错", font=font, fill=(0, 0, 0) )
    im1.paste ( a_imgb, (100, 130) )
    draw = ImageDraw.Draw ( im1, "RGB" )

    draw.text ( (370, 130), f"{dic.get ( '昵称' )}", (255, 255, 255), font=font )
    draw.text ( (370, 220), f"{dic.get ( '等级' )}", (255, 255, 255), font=font )
    draw.text ( (370, 310), f"{dic.get ( '游玩时间' )}", (255, 255, 255), font=font )

    draw.text ( (140, 450), f"{dic.get ( '击杀' )}", (255, 255, 255), font=font )
    draw.text ( (290, 450), f"{dic.get ( '助攻' )}", (255, 255, 255), font=font )
    draw.text ( (430, 450), f"{dic.get ( 'KD' )}", (255, 255, 255), font=font )
    draw.text ( (580, 450), f"{dic.get ( 'KPM' )}", (255, 255, 255), font=font )

    draw.text ( (140, 590), f"{dic.get ( '步战KD' )}", (255, 255, 255), font=font )
    draw.text ( (290, 590), f"{dic.get ( '步战KPM' )}", (255, 255, 255), font=font )
    draw.text ( (430, 590), f"{dic.get ( '爆头击杀' )}", (255, 255, 255), font=font )
    draw.text ( (580, 590), f"{dic.get ( '爆头率' )}", (255, 255, 255), font=font )

    draw.text ( (140, 730), f"{dic.get ( '精准率' )}", (255, 255, 255), font=font )
    draw.text ( (290, 730), f"{dic.get ( '胜场' )}", (255, 255, 255), font=font )
    draw.text ( (430, 730), f"{dic.get ( '败场' )}", (255, 255, 255), font=font )
    draw.text ( (580, 730), f"{dic.get ( '胜率' )}", (255, 255, 255), font=font )

    draw.text ( (140, 870), f"{dic.get ( '游戏局数' )}", (255, 255, 255), font=font )
    draw.text ( (280, 870), f"{dic.get ( 'SPM' )}", (255, 255, 255), font=font )
    draw.text ( (430, 870), f"{dic.get ( '技巧值' )}", (255, 255, 255), font=font )
    draw.text ( (580, 870), f"{dic.get ( '总医疗量' )}", (255, 255, 255), font=font )

    plt.imshow ( im1 )
    plt.show ()
    im1.save ( "src/plugins/BF1_record/record.png" )


img_path = 'file:///' + os.path.split(os.path.realpath(__file__))[0]+'/'

def send_img(img_name):
    global img_path
    return MessageSegment.image(img_path + img_name)

   
    
@BFIS.handle()
async def BFIG(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = event.message.extract_plain_text ().replace ( "BFI", "" )
    if not msg:
        await BFIS.finish ( "战绩查询+游戏ID" )
    get_data ( msg )
    draw_img ()
    # img="src/plugins/BF1_record/record.png"
    await BFIS.send(Message('详细数据访问:'+'https://battlefieldtracker.com/bf1/profile/pc/'+f'{msg}'))
    await BFIS.send(send_img("record.png"))
    
@BFIS.handle()
async def BFIQ(bot: Bot, event: PrivateMessageEvent, state: T_State):
    msg = event.message.extract_plain_text ().replace ( "BFI", "" )
    if not msg:
        await BFIS.finish ( "战绩查询+游戏ID" )
    get_data ( msg )
    draw_img ()
    # img="src/plugins/BF1_record/record.png"
    await BFIS.send(Message('详细数据访问:'+'https://battlefieldtracker.com/bf1/profile/pc/'+f'{msg}'))
    await BFIS.send(send_img("record.png"))
    # pathlib.Path('file_path').as_uri()

@BFVS.handle()
async def BFIG(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = event.message.extract_plain_text ().replace ( "BFV", "" )
    if not msg:
        await BFVS.finish ( "战绩查询+游戏ID" )
    get_dataV ( msg )
    draw_img ()
    # img="src/plugins/BF1_record/record.png"
    # await BFVS.send(Message('https://battlefieldtracker.com/bfv/profile/origin/'+f'{msg}'+'/overview'))
    await BFVS.send(Message('详细数据访问:'+'https://battlefieldtracker.com/bfv/profile/origin/'+f'{msg}'+'/overview'))
    await BFVS.send(send_img("record.png"))

@BFVS.handle()
async def BFIQ(bot: Bot, event: PrivateMessageEvent, state: T_State):
    msg = event.message.extract_plain_text ().replace ( "BFV", "" )
    if not msg:
        await BFVS.finish ( "战绩查询+游戏ID" )
    get_dataV ( msg )
    draw_img ()
    # img="src/plugins/BF1_record/record.png"
    await BFVS.send(Message('详细数据访问:'+'https://battlefieldtracker.com/bfv/profile/origin/'+f'{msg}'+'/overview'))
    await BFVS.send(send_img("record.png"))
    # pathlib.Path('file_path').as_uri()    