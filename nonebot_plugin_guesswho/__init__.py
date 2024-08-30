from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require
from .config import ConfigModel

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
