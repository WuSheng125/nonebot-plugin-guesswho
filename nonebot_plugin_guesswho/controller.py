import os
import json
from pathlib import Path

from .config import config

COOLDOWN_TIME = config.guesswho_cooldow
PLAYERDATA_PATH = config.guesswho_playerdata_path
COINGET = config.guesswho_coin_get


class Controller:
    """游戏控制器，存储与更改各个群的游戏状态"""
    def __init__(self):
        self.status = {}
        self.time = {}
        self.flag = {}
        self.coin = {}

        if os.path.exists(PLAYERDATA_PATH):
            with open(PLAYERDATA_PATH, 'r', encoding='utf-8') as file:
                self.coin = json.load(file)

    def start(self, group_id):
        if self.status.get(group_id):
            return True
        else:
            self.status[group_id] = True
            return False

    def end(self, group_id, user_id=None):
        cropped_img_path = Path(__file__).parent / 'data' / (group_id + '_tmp.png')
        os.remove(cropped_img_path)
        self.status[group_id] = False
        if user_id is not None:
            if self.coin.get(user_id) is None:
                self.coin[user_id] = COINGET
            else:
                self.coin[user_id] += COINGET
            with open(PLAYERDATA_PATH, 'w', encoding='utf-8') as file:
                file.write(json.dumps(self.coin, indent=4, ensure_ascii=False))
            return COINGET, self.coin[user_id]

    def update(self, user_id, group_id, time):
        if COOLDOWN_TIME == 0:
            return 0

        if self.status.get(group_id):
            return -1

        if self.time.get(group_id) is None:
            self.time[group_id] = {user_id: time}
            self.flag[group_id] = {user_id: False}
            return 0

        if self.time[group_id].get(user_id) is None:
            self.time[group_id][user_id] = time
            self.flag[group_id][user_id] = False
            return 0

        cd = COOLDOWN_TIME - (time - self.time[group_id][user_id])
        if cd <= 0:
            self.time[group_id][user_id] = time
            self.flag[group_id][user_id] = False
            return 0

        if self.flag[group_id][user_id]:
            return -2
        else:
            self.flag[group_id][user_id] = True
            return int(cd)


controller = Controller()
