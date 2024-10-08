from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require
from nonebot.plugin.on import on_command
from nonebot.rule import is_type
from nonebot import get_driver

from .handler import *
from .check import data_check
from .config import ConfigModel, config

require("nonebot_plugin_alconna")

prefix: str = next(iter(config.command_start))
__version__ = "0.1.0"
__plugin_meta__ = PluginMetadata(
    name="猜角色",
    description="来一场猜角色小游戏吧~",
    usage=f"""碧蓝航线：{prefix}猜舰娘+[tag]，不指定tag时范围为所有
例：{prefix}猜舰娘 / {prefix}猜舰娘海上传奇 / {prefix}猜舰娘重樱
明日方舟：{prefix}猜干员+[tag]，不指定tag时范围为所有
例：{prefix}猜干员 / {prefix}猜干员近卫 / {prefix}猜干员莱茵生命\n\n
蔚蓝档案：{prefix}猜学生+[tag]，不指定tag时范围为所有
例：{prefix}猜学生 / {prefix}猜学生千禧年 / {prefix}猜学生支援""",
    type="application",
    homepage="https://github.com/WuSheng125/nonebot-plugin-guesswho",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "MIT", "Author": "WuSheng125"},
)

get_driver().on_startup(data_check)

if config.guesswho_enabled['azurlane']:
    on_command(cmd="猜舰娘",
               block=True,
               priority=5,
               rule=is_type(GroupMessageEvent),
               handlers=[azurlane_guess])

if config.guesswho_enabled['arknights']:
    on_command(cmd="猜干员",
               block=True,
               priority=5,
               rule=is_type(GroupMessageEvent),
               handlers=[arknights_guess])

if config.guesswho_enabled['bluearchive']:
    on_command(cmd="猜学生",
               block=True,
               priority=5,
               rule=is_type(GroupMessageEvent),
               handlers=[bluearchive_guess])
