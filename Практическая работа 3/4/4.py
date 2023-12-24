import zipfile
import os
from bs4 import BeautifulSoup
import numpy as np
import json
import shutil


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

        root = BeautifulSoup(text, 'xml')

        for clothing in root.find_all("clothing"):
            item = dict()
            for el in clothing.contents:
                if el.name is None:
                    continue
                elif el.name == "price" or el.name == "reviews":
                    item[el.name] = int(el.get_text().strip())
                elif el.name == "rating":
                    item[el.name] = float(el.get_text().strip())
                elif el.name == "new":
                    item[el.name] = el.get_text().strip() == "+"
                elif el.name == "exclusive" or el.name == "sporty":
                    item[el.name] = el.get_text().strip() == "yes"
                else:
                    item[el.name] = el.get_text().strip()

            items.append(item)

        return items


zip_path = 'zip_var_49.zip'

# Распаковка zip-архива
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('temp_folder')

items = []

# Проходим по всем файлам в распакованной папке
folder_path = 'temp_folder'
for filename in os.listdir(folder_path):
    if filename.endswith(".xml"):
        result = handle_file(f'{folder_path}\{filename}')
        items += result

# Удаляем временную папку с распакованными файлами
shutil.rmtree(folder_path)

items = sorted(items, key=lambda x: x['price'], reverse=True)

filtered_items = []
for item in items:
    if item['rating'] >= 5:
        filtered_items.append(item)

num_stat = get_num_stat("price", items)
size_freq = get_freq("size", items)

write_to_json("result_all.json", items)
write_to_json("result_filtered.json", filtered_items)
write_to_json("result_num_stat.json", num_stat)
write_to_json("result_size_freq.json", size_freq)