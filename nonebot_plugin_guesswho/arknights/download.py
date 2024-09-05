import json
import os
from httpx import AsyncClient
from bs4 import BeautifulSoup

from ..config import config


def parse_element(element):
    data = {
        'tag': element.name,
        'text': element.get_text(strip=True),
        'attributes': element.attrs,
        'children': []
    }

    # 递归处理
    for child in element.children:
        if child.name:
            data['children'].append(parse_element(child))

    return data


async def get_data():
    async with AsyncClient(
            follow_redirects=True,
            proxies="",
            timeout=5,
    ) as client:
        res_tujian = await client.get("https://prts.wiki/w/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88")
        res_tujian.raise_for_status()

    soup_tujian = BeautifulSoup(res_tujian.text, 'html.parser')
    div = soup_tujian.find('div', id='filter-data')
    characters = parse_element(div)['children']

    parsed_data = {}
    for element in characters:
        tags = [
            element['attributes']['data-profession'],
            element['attributes']['data-subprofession'],
            element['attributes']['data-logo'],
            element['attributes']['data-birth_place'],
            element['attributes']['data-race'],
            element['attributes']['data-position']
        ] + element['attributes']['data-tag'].split()
        character = {
            'name-en': element['attributes']['data-en'],
            'name-jp': element['attributes']['data-ja'],
            'id': element['attributes']['data-id'],
            'tags': [x for x in tags if x]
        }
        parsed_data[element['attributes']['data-zh']] = character

    return parsed_data


async def arknights_download():
    data = await get_data()

    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    os.makedirs(config.guesswho_arknights_picpath, exist_ok=True)
    json_path = config.guesswho_arknights_picpath / "data.json"
    with open(json_path, "w", encoding="utf-8") as file:
        file.write(json_data)
