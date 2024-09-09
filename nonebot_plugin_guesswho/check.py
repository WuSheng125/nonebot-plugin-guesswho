import os
import json
from pathlib import Path

from nonebot import logger

from .config import config


def data_check():
    for game_type in config.guesswho_enabled:
        if config.guesswho_enabled[game_type]:
            check(game_type)


def check(game_type: str):
    json_path = Path(__file__).parent / 'data' / (game_type + '_data.json')
    pic_path = config.guesswho_picpath[game_type]
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    missing_resources = []
    for character in data:
        if not os.path.exists(pic_path / character):
            missing_resources.append(character)
            continue
        if len(os.listdir(pic_path / character)) == 0:
            missing_resources.append(character)
    if len(missing_resources) != 0:
        logger.warning(missing_resources)
        logger.warning("资源文件缺失，请检查资源文件目录！")
