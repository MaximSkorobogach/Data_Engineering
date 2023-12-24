import zipfile
import os
from bs4 import BeautifulSoup
import numpy as np
import json
import re

def get_num_stat(selector: str, items: list):
    nums = list(map(lambda x: float(x[selector]), items))

    stat = {}

    stat['sum'] = sum(nums)
    stat['min'] = min(nums)
    stat['max'] = max(nums)
    stat['avg'] = np.average(nums)
    stat['std'] = np.std(nums)

    return stat


def get_freq(selector: str, items: list):
    freq = {}

    for item in items:
        if selector in item:
            freq[item[selector]] = freq.get(item[selector], 0) + 1

    return freq

def write_to_json(path: str, data: str):
    with open(path, 'w', encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False))

def handle_file(file_name):
    items = list()

    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        products = site.find_all("div", attrs={'class': 'product-item'})

        for product in products:
            item = dict()
            item['id'] = product.a['data-id']
            item['link'] = product.find_all('a')[1]['href']
            item['img_url'] = product.find_all('img')[0]['src']
            item['title'] = product.find_all('span')[0].get_text().strip()
            item['price'] = int(product.price.get_text().replace("₽", "").replace(" ", "").strip())
            item['bonus'] = int(product.strong.get_text().replace("+ начислим ", "").replace(" бонусов", "").strip())
            props = product.ul.find_all("li")
            for prop in props:
                item[prop['type']] = prop.get_text().strip()

            items.append(item)

        return items


# Путь к zip-архиву с HTML-файлами
zip_path = 'zip_var_49.zip'  # Замените на реальный путь

# Распаковка zip-архива
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('temp_folder')

items = []

# Проходим по всем файлам в распакованной папке
folder_path = 'temp_folder'
for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        result = handle_file(f'{folder_path}\{filename}')
        items += result;

# Удаляем временную папку с распакованными файлами
import shutil
shutil.rmtree(folder_path)

items = sorted(items, key=lambda x: x['bonus'], reverse=True)

filtered_items = []
for item in items:
    if item['price'] >= 490000:
        filtered_items.append(item)

num_stat = get_num_stat("price", items)
title_freq = get_freq("ram", items)

write_to_json("result_all.json", items)
write_to_json("result_filtered.json", filtered_items)
write_to_json("result_num_stat.json", num_stat)
write_to_json("result_title_freq.json", title_freq)