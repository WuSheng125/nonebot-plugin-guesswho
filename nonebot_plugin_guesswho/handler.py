from nonebot.adapters.onebot.v11 import Message, Event, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.rule import to_me
from nonebot_plugin_waiter import waiter

from .utils import controller
from .azurlane import get_randchar


async def azurlane_guess(matcher: Matcher, event: Event, args: Message = CommandArg()):
    group_id = event.get_session_id()
    tag = args.extract_plain_text().strip()
    if controller.start(group_id):
        await matcher.finish("有正在进行中的游戏哦！")
    names, full_img, cropped_img = get_randchar(group_id, tag)
    if names is None:
        controller.end(group_id)
        msg = Message() + MessageSegment.text(f"不存在具有tag{tag}的舰娘哦，请重新开始游戏")
        await matcher.finish(msg)
    msg = Message() + MessageSegment.image(cropped_img) + MessageSegment.text("这是哪位舰娘？")
    msg += MessageSegment.text("\n120秒内@我发送你的答案(共有三次机会)\n@我发送[退出]以直接结束游戏")
    await matcher.send(msg)

    @waiter(waits=["message"], block=True, rule=to_me(), keep_session=False)
    async def listen(_event: Event):
        text = _event.get_message().extract_plain_text()
        if text == "退出":
            return False
        return text

    end_msg = Message() + MessageSegment.image(full_img)
    async for resp in listen(timeout=120, retry=2, prompt=''):
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
            await matcher.send(f"她不是{resp}呢")
    else:
        controller.end(group_id)
        end_msg += MessageSegment.text(f"没猜出来呢，下次再加油吧~本题的答案是{names[0]}哦~")
        await matcher.finish(end_msg)


async def arknights_guess(matcher: Matcher, args: Message = CommandArg()):
    pass


async def bluearchive_guess(matcher: Matcher, args: Message = CommandArg()):
    pass
