import random
import json
import os
import math
from PIL import Image, ImageFile

from ..config import config


def get_alpha_ratio(img: ImageFile):
    datas = img.getdata()
    non_transparent_pixels = len([pixel for pixel in datas if pixel[3] != 0])
    total_pixels = img.size[0] * img.size[1]
    non_transparency_ratio = non_transparent_pixels / total_pixels
    return non_transparency_ratio


def get_randchar(group_id, tag: str = ''):
    path = config.guesswho_azurlane_picpath
    with open(path / 'data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    char_range = []
    if tag == '':
        char_range = [x for x in data]
    else:
        for char in data:
            if tag in data[char]['tags']:
                char_range.append(char)
    if not char_range:
        return None, None, None

    selected_char = random.choice(char_range)
    selected_img_path = path / selected_char / random.choice(os.listdir(path / selected_char))
    selected_img = Image.open(selected_img_path)

    width, height = selected_img.size
    while True:
        left = math.floor(random.random() * (width - 0.28 * width))
        bottom = math.floor(random.random() * (height - 0.28 * height))
        cropped_img = selected_img.crop((left, bottom, left + 0.28 * width, bottom + 0.28 * height))
        if get_alpha_ratio(cropped_img) > 0.5:
            cropped_img_path = path / (group_id + '_tmp.png')
            cropped_img.save(cropped_img_path)
            return data[selected_char]['names'], selected_img_path, cropped_img_path
