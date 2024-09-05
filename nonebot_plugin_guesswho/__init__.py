from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require
from nonebot.plugin.on import on_command
from nonebot import get_driver

from .handler import *
from .config import ConfigModel, config
from .azurlane import azurlane_download
from .arknights import arknights_download

require("nonebot_plugin_alconna")

__version__ = "0.1.0"
__plugin_meta__ = PluginMetadata(
    name="猜角色",
    description="来一场猜角色小游戏吧~",
    usage="待定",
    type="application",
    homepage="https://github.com/WuSheng125/nonebot-plugin-guesswho",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "MIT", "Author": "WuSheng125"},
)

driver = get_driver()

if config.guesswho_azurlane_enabled:
    driver.on_startup(azurlane_download)
    on_command(cmd="猜舰娘",
               block=True,
               priority=5,
               handlers=[azurlane_guess])

if config.guesswho_arknights_enabled:
    driver.on_startup(arknights_download)
    on_command(cmd="猜干员",
               block=True,
               priority=5,
               handlers=[arknights_guess])

if config.guesswho_bluearchive_enabled:
    on_command(cmd="猜学生",
               block=True,
               priority=5,
               handlers=[bluearchive_guess])
