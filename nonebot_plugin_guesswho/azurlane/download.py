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
        res_tujian = await client.get("https://wiki.biligame.com/blhx/%E8%88%B0%E8%88%B9%E5%9B%BE%E9%89%B4")
        res_tujian.raise_for_status()
        res_skins = await client.get("https://wiki.biligame.com/blhx/%E6%8D%A2%E8%A3%85%E5%9B%BE%E9%89%B4")
        res_skins.raise_for_status()

    soup_tujian = BeautifulSoup(res_tujian.text, 'html.parser')
    divs = soup_tujian.find_all('div', class_='jntj-1 divsort')
    div_data = []
    for div in divs:
        div_data.append(parse_element(div))

    parsed_data = {}
    for element in div_data:
        character = {
            "names": list(filter(lambda string: string != '', [
                element['children'][-1]['children'][0]['attributes']['title'],
                element['text'].replace(element['children'][-1]['children'][0]['attributes']['title'], '')
            ])),
            "tags": list(filter(lambda string: string != '',
                                element['attributes']['data-param1'].split(",,") + [
                                    element['attributes']['data-param2'],
                                    element['attributes']['data-param3']
                                ] + element['attributes']['data-param4'].split(","))),
            "skins": ['原始'],
            "url": "https://wiki.biligame.com" + element['children'][-1]['children'][0]['attributes']['href']
        }
        if "改造" not in character["tags"]:
            if " 誓约" in character["tags"]:
                character["tags"].remove(" 誓约")
                character["tags"].append("誓约")
            parsed_data[character["names"][0]] = character
        else:
            parsed_data[element['children'][-1]['children'][0]['attributes']['title']]["skins"].append("改造")

    soup_skins = BeautifulSoup(res_skins.text, 'html.parser')
    spans = soup_skins.find_all('span', class_='popup')
    for span in spans:
        span_parsed = parse_element(span)
        name = span_parsed["text"].split('- 「')
        parsed_data[name[0]]["skins"].append(name[1][:-1])

    return parsed_data


async def azurlane_download():
    data = await get_data()

    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    os.makedirs(config.guesswho_azurlane_picpath, exist_ok=True)
    json_path = config.guesswho_azurlane_picpath / "data.json"
    with open(json_path, "w", encoding="utf-8") as file:
        file.write(json_data)
