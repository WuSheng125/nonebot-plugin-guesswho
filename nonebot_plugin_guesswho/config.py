from pathlib import Path

from nonebot import get_plugin_config
from pydantic import BaseModel


class ConfigModel(BaseModel):
    guesswho_azurlane_enabled: bool = True
    guesswho_azurlane_picpath: Path = Path() / 'data' / 'nonebot_plugin_guesswho' / 'azurlane'
    guesswho_arknights_enabled: bool = True
    guesswho_arknights_picpath: Path = Path() / 'data' / 'nonebot_plugin_guesswho' / 'arknights'
    guesswho_bluearchive_enabled: bool = True
    guesswho_bluearchive_picpath: Path = Path() / 'data' / 'nonebot_plugin_guesswho' / 'bluearchive'


config: ConfigModel = get_plugin_config(ConfigModel)
