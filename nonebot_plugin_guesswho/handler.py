from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

from .utils import game_process


async def azurlane_guess(matcher: Matcher, event: GroupMessageEvent, args: Message = CommandArg()):
    await game_process(matcher, event, game_type='azurlane', tag=args.extract_plain_text().strip())


async def arknights_guess(matcher: Matcher, event: GroupMessageEvent, args: Message = CommandArg()):
    await game_process(matcher, event, game_type='arknights', tag=args.extract_plain_text().strip())


async def bluearchive_guess(matcher: Matcher, args: Message = CommandArg()):
    pass
