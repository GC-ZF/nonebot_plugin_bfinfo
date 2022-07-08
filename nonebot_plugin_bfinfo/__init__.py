"""
@Author:张时贰
@Date:2022年07月04日
@CSDN:张时贰
@Blog:zhangshier.vip
"""
'''
PIL学习
https://blog.csdn.net/qq_41780234/article/details/122242664?ops_request_misc=&request_id=&biz_id=102&utm_term=python%E5%B0%86%E6%96%87%E5%AD%97%E5%86%99%E5%9C%A8%E5%9B%BE%E7%89%87%E4%B8%8A&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-1-122242664.142^v24^huaweicloudv2,157^v15^new_3&spm=1018.2226.3001.4187
'''
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, GroupMessageEvent, Message
import json
import io, os
from PIL import ImageFont, Image, ImageDraw
import requests
from pylab import *
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment

BFIS = on_command ( "BFI", block=True, priority=12 )
BFVS = on_command ( "BFV", block=True, priority=12 )

get_json = ""
filepath = os.path.dirname ( __file__ )
bf1_imgpath = os.path.join ( filepath, "bf1" )  # bf1图片路径
bfv_imgpath = os.path.join ( filepath, "bfv" )  # bfv图片路径
transtxt_path = os.path.join ( filepath, "bf_translate.json" )
font_path = os.path.join ( filepath, "STXINGKA.TTF" )  # 文字样式
largefont = ImageFont.truetype ( font_path, 38 )  # 文字大小
type_dict = {"weapon": "weapons", "vehicle": "vehicles", "class": "classes"}


# 转换秒数为时分秒的形式
def seconds_trans(seconds):
    m, s = divmod ( seconds, 60 )
    h, m = divmod ( m, 60 )
    return "%02d时%02d分%02d秒"%(h, m, s)


def resize_font(font_size, text_str, limit_width):
    '''
    在给定的长度内根据文字内容来改变文字的字体大小
    font_size为默认大小,即如果函数判断以此字体大小所绘制出来的文字内容不会超过给定的长度时,则保持这个大小
    若绘制出来的文字内容长度大于给定长度,则会不断对减小字体大小直至刚好小于给定长度
    text_str为文字内容
    limit_width为给定的长度
    返回内容为PIL.ImageFont.FreeTypeFont对象
    '''

    font = ImageFont.truetype ( font_path, font_size )
    font_lenth = font.getsize ( str ( text_str ) )[ 0 ]
    while font_lenth > limit_width:
        font_size -= 1
        font = ImageFont.truetype ( font_path, font_size )
        font_lenth = font.getsize ( text_str )[ 0 ]

    return font


# 通过API获取ID信息
def get_data(player_name, bfversion):
    global get_json
    if bfversion == "bf1":
        url = f"https://api.gametools.network/bf1/all/?name={player_name}&lang=en-us"
    elif bfversion == "bfv":
        url = f"https://api.gametools.network/bfv/all/?name={player_name}&lang=en-us"
    get_data = requests.get ( url )
    get_json = json.loads ( get_data.text )


with open ( transtxt_path, 'r', encoding='utf-8' ) as f:
    bf1translate = json.loads ( f.read () )


# 返回文字内容（除去名称和类型）以及文字内容的长度
def dict_text_draw_info(select_dict):
    text = ""
    text_lenth = 0
    for k, v in select_dict.items ():
        if k == "名称" or k == '类型':
            continue
        text += f'{k}:{str ( v )}   '

    font = resize_font ( 38, text, 1000 )
    text_lenth = font.getsize ( text.strip () )[ 0 ]

    return text, text_lenth


# 返回图标路径,图标透明度,将图标宽度拉至100像素后对应的长度,图标名称
def icon_info(bfversion, mode, dict):
    if bfversion == "bf1":
        img_path = bf1_imgpath
    elif bfversion == "bfv":
        img_path = bfv_imgpath
    icon_name = dict.get ( '名称' )
    try:
        if mode == "class":
            im = Image.open ( os.path.join ( img_path, 'class_img', icon_name + '.png' ) )
        elif mode == "weapon":
            im = Image.open ( os.path.join ( img_path, 'weapon_img', dict.get ( '类型' ), icon_name + '.png' ) )
        elif mode == "vehicle":
            im = Image.open ( os.path.join ( img_path, 'vehicle_img', dict.get ( '类型' ), icon_name + '.png' ) )
    except FileNotFoundError:
        raise Exception ( mode )
    size = im.size
    x, y = int ( size[ 0 ]*(100/size[ 1 ]) ), 100
    icon_path = im.resize ( (x, y) )
    return icon_path, icon_path.split ()[ 3 ], x, icon_name.replace ( '_', '/' )


# 将详细数据绘制到图片中
def bestinfo_drawer(bfversion, mode, image, dict, middle_x, y, blank):
    icon1 = icon_info ( bfversion, mode, dict )
    image.paste ( icon1[ 0 ], (middle_x - icon1[ 2 ] - 20, y), icon1[ 1 ] )
    draw = ImageDraw.Draw ( image, "RGB" )
    transtext = bf1translate.get ( str ( icon1[ 3 ] ).upper (), icon1[ 3 ] )
    draw.text ( (middle_x + 20, y + 25), transtext, font=resize_font ( 38, transtext, 490 ), fill=(255, 255, 255) )
    draw1 = dict_text_draw_info ( dict )
    draw.text ( (middle_x - draw1[ 1 ]/2, y + blank + 100), draw1[ 0 ], font=resize_font ( 38, draw1[ 0 ], 1000 ),
                fill=(255, 255, 255) )


# 对基本数据处理为字典
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


# 找出最佳兵种信息
def best_class():
    class_list = [ ]
    class_page = get_json[ 'classes' ]
    for i in class_page:
        class_dict = {}
        class_dict[ '名称' ] = i[ 'className' ]
        class_dict[ '击杀' ] = i[ 'kills' ]
        # class_dict[ 'img' ] = i['image']
        class_dict[ 'KPM' ] = i[ 'kpm' ]
        class_dict[ '得分' ] = i[ 'score' ]
        class_dict[ '时长' ] = seconds_trans ( i[ 'secondsPlayed' ] )
        class_list.append ( class_dict )
    class_list.sort ( key=lambda x: x[ '击杀' ], reverse=True )  # 排序

    return class_list


# 最佳武器信息
def best_weapon():
    general_weapon_list, Gadget_list, Sidearm_list, Field_kit_list, Melee_list = [ ], [ ], [ ], [ ], [ ]
    weapon_page = get_json[ 'weapons' ]
    for i in weapon_page:
        weapon_dict = {}
        weapon_dict[ '名称' ] = i[ 'weaponName' ].replace ( '/', '_' )
        weapon_dict[ '击杀' ] = i[ 'kills' ]
        weapon_dict[ 'KPM' ] = i[ 'killsPerMinute' ]
        weapon_dict[ '爆头率' ] = i[ 'headshots' ]
        weapon_dict[ '精准率' ] = i[ 'accuracy' ]
        weapon_dict[ '时长' ] = seconds_trans ( i[ 'timeEquipped' ] )
        weapon_dict[ '类型' ] = i[ 'type' ].replace ( '/', '_' )
        general_weapon_list.append ( weapon_dict )
    general_weapon_list.sort ( key=lambda x: x[ '击杀' ], reverse=True )  # 按击杀排序
    # Gadget_list.extend(i for i in general_weapon_list if i.get('类型') == "Gadget")
    # Sidearm_list.extend(i for i in general_weapon_list if i.get('类型') == "Sidearm")
    # Field_kit_list.extend(i for i in general_weapon_list if i.get('类型') == "Field kit")
    # Melee_list.extend(i for i in general_weapon_list if i.get('类型') == "Melee")

    return general_weapon_list


# 最佳载具信息
def best_vehicles():
    vehicle_lsit = [ ]
    vehicle_page = get_json[ 'vehicles' ]
    for i in vehicle_page:
        vehicle_dict = {}
        vehicle_dict[ '击杀' ] = i[ 'kills' ]
        vehicle_dict[ 'KPM' ] = i[ 'killsPerMinute' ]
        vehicle_dict[ '时长' ] = seconds_trans ( i[ 'timeIn' ] )
        vehicle_dict[ '类型' ] = i[ 'type' ].replace ( '/', '_' )
        vehicle_dict[ '名称' ] = i[ 'vehicleName' ].replace ( '/', '_' )
        vehicle_lsit.append ( vehicle_dict )
    vehicle_lsit.sort ( key=lambda x: x[ '击杀' ], reverse=True )

    return vehicle_lsit


# 最佳模式
def best_gamemodes():
    modes_list = [ ]
    modes_page = get_json[ 'gamemodes' ]
    for i in modes_page:
        modes_dict = {}
        modes_dict[ '胜场' ] = i[ 'wins' ]
        modes_dict[ '败场' ] = i[ 'losses' ]
        modes_dict[ '胜率' ] = i[ 'winPercent' ]
        modes_dict[ '得分' ] = i[ 'score' ]
        modes_dict[ '名称' ] = i[ 'gamemodeName' ]
        modes_list.append ( modes_dict )
    modes_list.sort ( key=lambda x: x[ '得分' ], reverse=True )

    return modes_list


# 异常处理，本地图片缺失，从api下载缺失图片
def img_completer(bfversion, img_type):
    if bfversion == "bf1":
        img_path = os.path.join ( bf1_imgpath, f"{img_type}_img" )
    elif bfversion == "bfv":
        img_path = os.path.join ( bfv_imgpath, f"{img_type}_img" )

    local_img_list = [ ]
    api_img_list = [ ]
    for i in os.walk ( os.path.join ( bfv_imgpath, img_type + "_img" ) ):
        local_img_list += i[ 2 ]
    for i in range ( len ( local_img_list ) ):
        local_img_list[ i ] = local_img_list[ i ].replace ( ".png", "" )
    api_img = get_json[ type_dict.get ( img_type ) ]
    for i in api_img:
        name = i[ f'{img_type}Name' ].replace ( '/', '_' )
        api_img_list.append ( name )
    a = set ( api_img_list )
    b = set ( local_img_list )
    compare_list = list ( b ^ a )
    for i in api_img:
        name = i[ f'{img_type}Name' ].replace ( '/', '_' )
        if name in compare_list:
            img = i[ 'image' ]
            get_type = i[ 'type' ].replace ( '/', '_' )
            print ( f"正在补全{img_type}第{compare_list.index ( name ) + 1}个图标" )
            geturl = requests.get ( img )
            img_content = geturl.content
            img_bytestream = io.BytesIO ( img_content )
            im = Image.open ( img_bytestream )

            bbox = im.getbbox ()
            middle_point = ((bbox[ 0 ] + bbox[ 2 ])/2, (bbox[ 1 ] + bbox[ 3 ])/2)
            if bbox[ 2 ] - bbox[ 0 ] <= 256 and bbox[ 3 ] - bbox[ 1 ] <= 64:
                crop_box = (
                    middle_point[ 0 ] - 128, middle_point[ 1 ] - 32, middle_point[ 0 ] + 128, middle_point[ 1 ] + 32)
            elif bbox[ 2 ] - bbox[ 0 ] > 256 and bbox[ 3 ] - bbox[ 1 ] > 64:
                crop_box = (bbox[ 0 ] - 10, bbox[ 1 ] - 10, bbox[ 2 ] + 10, bbox[ 3 ] + 10)
            else:
                if bbox[ 2 ] - bbox[ 0 ] > 256:
                    crop_box = (bbox[ 0 ] - 10, middle_point[ 1 ] - 32, bbox[ 2 ] + 10, middle_point[ 1 ] + 32)
                elif bbox[ 3 ] - bbox[ 1 ] > 64:
                    crop_box = (middle_point[ 0 ] - 128, bbox[ 1 ] - 10, middle_point[ 0 ] + 128, bbox[ 3 ] + 10)
            im2 = im.crop ( crop_box )
            print ( f"{img_path}/{get_type}/{name}.png" )
            im2.save ( f"{img_path}/{get_type}/{name}.png" )


# 绘制图像
def draw_img(bfversion):
    dic_base = general ()  # 获取基本数据
    list_class = best_class ()  # 获取最佳兵种
    list_weapon = best_weapon ()  # 获取最佳武器
    list_vehicle = best_vehicles ()  # 最佳载具
    # list_modes = best_gamemodes ()  # 最佳游戏模式
    # 设置字体，如果没有，也可以不设置
    font = ImageFont.truetype ( f"{filepath}" + "/STXINGKA.TTF", 38 )

    # 打开背景图片
    imageFile = f"{filepath}" + "/general_bg.jpg"
    im1 = Image.open ( f"{imageFile}" )

    # 在图片上添加文字
    draw = ImageDraw.Draw ( im1 )

    try:
        geturl = dic_base.get ( '头像img' )
        geturl = requests.get ( geturl )
        a = geturl.content
        aimg_bytestream = io.BytesIO ( a )
        a_imgb = Image.open ( aimg_bytestream ).resize ( (230, 230) )
    except:
        a_imgb = Image.new ( "RGB", (230, 230), (255, 255, 255) )
        a_draw = ImageDraw.Draw ( a_imgb, "RGB" )
        a_draw.text ( (38, 94), "头像获取出错", font=font, fill=(0, 0, 0) )
    im1.paste ( a_imgb, (100, 130) )  # 将一张图片粘贴到另一张图片
    draw = ImageDraw.Draw ( im1, "RGB" )

    # 基础信息
    draw.text ( (370, 130), f"{dic_base.get ( '昵称' )}", (255, 255, 255), font=font )
    draw.text ( (370, 220), f"{dic_base.get ( '等级' )}", (255, 255, 255), font=font )
    draw.text ( (370, 310), f"{dic_base.get ( '游玩时间' )}", (255, 255, 255), font=font )

    draw.text ( (140, 450), f"{dic_base.get ( '击杀' )}", (255, 255, 255), font=font )
    draw.text ( (290, 450), f"{dic_base.get ( '助攻' )}", (255, 255, 255), font=font )
    draw.text ( (430, 450), f"{dic_base.get ( 'KD' )}", (255, 255, 255), font=font )
    draw.text ( (580, 450), f"{dic_base.get ( 'KPM' )}", (255, 255, 255), font=font )

    draw.text ( (140, 590), f"{dic_base.get ( '步战KD' )}", (255, 255, 255), font=font )
    draw.text ( (290, 590), f"{dic_base.get ( '步战KPM' )}", (255, 255, 255), font=font )
    draw.text ( (430, 590), f"{dic_base.get ( '爆头击杀' )}", (255, 255, 255), font=font )
    draw.text ( (580, 590), f"{dic_base.get ( '爆头率' )}", (255, 255, 255), font=font )

    draw.text ( (140, 730), f"{dic_base.get ( '精准率' )}", (255, 255, 255), font=font )
    draw.text ( (290, 730), f"{dic_base.get ( '胜场' )}", (255, 255, 255), font=font )
    draw.text ( (430, 730), f"{dic_base.get ( '败场' )}", (255, 255, 255), font=font )
    draw.text ( (580, 730), f"{dic_base.get ( '胜率' )}", (255, 255, 255), font=font )

    draw.text ( (140, 870), f"{dic_base.get ( '游戏局数' )}", (255, 255, 255), font=font )
    draw.text ( (280, 870), f"{dic_base.get ( 'SPM' )}", (255, 255, 255), font=font )
    draw.text ( (430, 870), f"{dic_base.get ( '技巧值' )}", (255, 255, 255), font=font )
    draw.text ( (580, 870), f"{dic_base.get ( '总医疗量' )}", (255, 255, 255), font=font )

    # 最佳兵种
    bestinfo_drawer ( bfversion, 'class', im1, list_class[ 0 ], 1310, 115, 10 )

    # 最佳枪械
    bestinfo_drawer ( bfversion, 'weapon', im1, list_weapon[ 0 ], 1310, 115 + 230*1, 10 )
    # 最佳载具
    bestinfo_drawer ( bfversion, 'vehicle', im1, list_vehicle[ 0 ], 1310, 115 + 230*2, 10 )
    # 最佳模式
    if bfversion == "bf1":
        list_modes = best_gamemodes ()  # 最佳游戏模式
        draw1 = dict_text_draw_info ( list_modes[ 0 ] )
        modename = f"最佳游戏模式:{bf1translate.get ( list_modes[ 0 ].get ( '名称' ).upper (), list_modes[ 0 ].get ( '名称' ) )}"
        draw.text ( (1310 - largefont.getsize ( modename )[ 0 ]/2, 110 + 230*3 + 25), modename, font=largefont,
                    fill=(255, 255, 255) )
        draw.text ( (1310 - draw1[ 1 ]/2, 110 + 230*3 + 115), draw1[ 0 ], font=resize_font ( 38, draw1[ 0 ], 1000 ),
                    fill=(255, 255, 255) )
    elif bfversion == "bfv":
        # bestinfo_drawer ( bfversion, 'weapon', im1, list_modes[ 0 ], 1310, 115 + 230*3, 10 )
        draw.text ( (1250, 850), "暂未修复", (255, 255, 255), font=font )

    plt.imshow ( im1 )
    plt.show ()
    im1.save ( f"{filepath}" + "/record.png" )


img_path = 'file:///' + os.path.split ( os.path.realpath ( __file__ ) )[ 0 ] + '/'


def send_img(img_name):
    global img_path
    return MessageSegment.image ( img_path + img_name )


@BFIS.handle ()
async def BFIG(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = event.message.extract_plain_text ().replace ( "BFI", "" )
    # msg += event.message.extract_plain_text ().replace ( " ", "" )
    if not msg:
        await BFIS.finish ( "战绩查询+游戏ID" )
    get_data ( msg, "bf1" )
    draw_img ( "bf1" )
    # img="src/plugins/BF1_record/record.png"
    await BFIS.send ( Message ( '详细数据访问:' + 'https://battlefieldtracker.com/bf1/profile/pc/' + f'{msg}' ) )
    await BFIS.send ( send_img ( "record.png" ) )


@BFIS.handle ()
async def BFIQ(bot: Bot, event: PrivateMessageEvent, state: T_State):
    msg = event.message.extract_plain_text ().replace ( "BFI", "" )
    if not msg:
        await BFIS.finish ( "战绩查询+游戏ID" )
    get_data ( msg, "bf1" )
    draw_img ( "bf1" )
    # img="src/plugins/BF1_record/record.png"
    await BFIS.send ( Message ( '详细数据访问:' + 'https://battlefieldtracker.com/bf1/profile/pc/' + f'{msg}' ) )
    await BFIS.send ( send_img ( "record.png" ) )
    # pathlib.Path('file_path').as_uri()


@BFVS.handle ()
async def BFVG(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = event.message.extract_plain_text ().replace ( "BFV", "" )
    # msg += event.message.extract_plain_text ().replace ( " ", "" )
    if not msg:
        await BFIS.finish ( "战绩查询+游戏ID" )
    get_data ( msg, "bfv" )
    draw_img ( "bfv" )
    # img="src/plugins/BF1_record/record.png"
    await BFIS.send ( Message ( '详细数据访问:' + 'https://battlefieldtracker.com/bfv/profile/pc/' + f'{msg}' ) )
    await BFIS.send ( send_img ( "record.png" ) )


@BFVS.handle ()
async def BFVQ(bot: Bot, event: PrivateMessageEvent, state: T_State):
    msg = event.message.extract_plain_text ().replace ( "BFV", "" )
    if not msg:
        await BFIS.finish ( "战绩查询+游戏ID" )
    get_data ( msg, "bfv" )
    draw_img ( "bfv" )
    # img="src/plugins/BF1_record/record.png"
    await BFIS.send ( Message ( '详细数据访问:' + 'https://battlefieldtracker.com/bfv/profile/pc/' + f'{msg}' ) )
    await BFIS.send ( send_img ( "record.png" ) )
    # pathlib.Path('file_path').as_uri()
