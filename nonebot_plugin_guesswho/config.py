from pathlib import Path
from typing import Set, Dict

from nonebot import get_plugin_config
from pydantic import BaseModel


class ConfigModel(BaseModel):
    command_start: Set[str] = ['/']

    guesswho_cooldow: int = 600
    guesswho_max_retries: int = 3
    guesswho_azurlane_enabled: bool = True
    guesswho_arknights_enabled: bool = True
    guesswho_bluearchive_enabled: bool = False
    guesswho_picpath: Dict = {
        'azurlane': Path() / 'data' / 'nonebot_plugin_guesswho' / 'azurlane',
        'arknights': Path() / 'data' / 'nonebot_plugin_guesswho' / 'arknights',
        'bluearchive': Path() / 'data' / 'nonebot_plugin_guesswho' / 'bluearchive'
    }


config: ConfigModel = get_plugin_config(ConfigModel)
