import random
import json
import os
import math
from PIL import Image, ImageFile
from pathlib import Path

from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent, MessageSegment
from nonebot.matcher import Matcher
from nonebot.rule import to_me, is_type
from nonebot_plugin_waiter import waiter

from .config import config
from .controller import controller

PICPATH = config.guesswho_picpath
RETRIES = config.guesswho_max_retries


async def game_process(
        matcher: Matcher,
        event: GroupMessageEvent,
        game_type: str,
        tag: str
):
    """游戏主进程"""
    group_id = event.get_session_id().split("_")[1]
    user_id = event.get_session_id().split("_")[2]

    cd = controller.update(user_id, group_id, event.time)
    if cd > 0:
        await matcher.finish(f"让人家歇会儿！冷却还有{cd}秒")
    elif cd == -1:
        await matcher.finish("有正在进行中的游戏哦！")
    elif cd == -2:
        return

    if controller.start(group_id):
        await matcher.finish("有正在进行中的游戏哦！")

    names, full_img, cropped_img = get_randchar(group_id, game_type, tag)
    if names is None:
        controller.end(group_id)
        msg = Message() + MessageSegment.text(f"不存在具有tag{tag}的角色哦，请重新开始游戏")
        await matcher.finish(msg)
    msg = Message() + MessageSegment.image(cropped_img) + MessageSegment.text("这是哪位角色？")
    msg += MessageSegment.text("\n120秒内@我发送你的答案(共有三次机会)\n@我发送[退出]以直接结束游戏")
    await matcher.send(msg)

    @waiter(waits=["message"], block=True, rule=to_me() & is_type(GroupMessageEvent), keep_session=False)
    async def listen(_event: GroupMessageEvent):
        """等待群友回复消息"""
        if _event.get_session_id().split("_")[1] != group_id:
            return
        text = _event.get_message().extract_plain_text()
        if text == "退出":
            return False
        return text

    end_msg = Message() + MessageSegment.image(full_img)
    async for resp in listen(timeout=120, retry=RETRIES-1, prompt=''):
        if resp is False:
            controller.end(group_id)
            end_msg += MessageSegment.text(f"游戏已取消!本题的答案是{names[0]}哦~")
            await matcher.finish(end_msg)
        if resp is None:
            controller.end(group_id)
            end_msg += MessageSegment.text(f"游戏已超时!本题的答案是{names[0]}哦~")
            await matcher.finish(end_msg)
        if resp in names:
            controller.end(group_id)
            end_msg += MessageSegment.text(f"答对啦！")
            await matcher.finish(end_msg)
        else:
            await matcher.send(f"不是{resp}呢")
    else:
        controller.end(group_id)
        end_msg += MessageSegment.text(f"没猜出来呢，下次再加油吧~本题的答案是{names[0]}哦~")
        await matcher.finish(end_msg)


def get_alpha_ratio(img: ImageFile):
    """获取不透明部分占比"""
    datas = img.getdata()
    non_transparent_pixels = len([pixel for pixel in datas if pixel[3] != 0])
    total_pixels = img.size[0] * img.size[1]
    non_transparency_ratio = non_transparent_pixels / total_pixels
    return non_transparency_ratio


def get_randchar(group_id, game_type: str, tag: str = ''):
    """获取指定游戏的随机角色"""
    path = PICPATH[game_type]
    json_path = Path(__file__).parent / 'data' / (game_type + '_data.json')
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    char_range = []
    if tag == '':
        char_range = [x for x in data]
    else:
        for char in data:
            if tag in data[char]['tags']:
                char_range.append(char)
    if not char_range:
        return None, None, None

    selected_char = random.choice(char_range)
    selected_img_path = path / selected_char / random.choice(os.listdir(path / selected_char))
    selected_img = Image.open(selected_img_path)

    width, height = selected_img.size
    while True:
        left = math.floor(random.random() * (width - 0.28 * width))
        bottom = math.floor(random.random() * (height - 0.28 * height))
        cropped_img = selected_img.crop((left, bottom, left + 0.28 * width, bottom + 0.28 * height))
        if get_alpha_ratio(cropped_img) > 0.5:
            cropped_img_path = Path(__file__).parent / 'data' / (group_id + '_tmp.png')
            cropped_img.save(cropped_img_path)
            return data[selected_char]['names'], selected_img_path, cropped_img_path
