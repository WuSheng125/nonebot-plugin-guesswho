import os
from pathlib import Path

from .config import config

COOLDOWN_TIME = config.guesswho_cooldow


class Controller:
    """游戏控制器，存储与更改各个群的游戏状态"""
    def __init__(self):
        self.status = {}
        self.time = {}
        self.flag = {}

    def start(self, group_id):
        if self.status.get(group_id):
            return True
        else:
            self.status[group_id] = True
            return False

    def end(self, group_id):
        cropped_img_path = Path(__file__).parent / 'data' / (group_id + '_tmp.png')
        os.remove(cropped_img_path)
        self.status[group_id] = False

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
