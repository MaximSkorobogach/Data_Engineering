import zipfile
import os
from bs4 import BeautifulSoup
import numpy as np
import json
import re
import shutil


#Получить статистику числовую
def get_num_stat(selector: str, items: list):
    nums = list(map(lambda x: float(x[selector]), items))

    stat = {}

    stat['sum'] = sum(nums)
    stat['min'] = min(nums)
    stat['max'] = max(nums)
    stat['avg'] = np.average(nums)
    stat['std'] = np.std(nums)

    return stat

#Получить статистику по тексту
def get_freq(selector: str, items: list):
    freq = {}

    for item in items:
        if selector in item:
            freq[item[selector]] = freq.get(item[selector], 0) + 1

    return freq

#Запись файла в JSON
def write_to_json(path: str, data: str):
    with open(path, 'w', encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False))

#Обработка файла
def handle_file(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')

        item = dict()

        address = site.find_all("p", attrs={"class": "address-p"})[0].get_text().split("Начало:")

        item['type'] = site.find_all("span", string=re.compile("Тип:"))[0].get_text().replace("Тип:", "").strip()
        item['title'] = site.find_all("h1")[0].get_text().replace("Турнир:\n", "").strip()
        item['city'] = address[0].replace("Город:", "").strip()
        item['date'] = address[1].strip()
        item['count'] = int(site.find_all("span", attrs={"class": "count"})[0].get_text().split(":")[1].strip())
        item['time'] = int(
            site.find_all("span", attrs={"class": "year"})[0].get_text().split(":")[1].replace("мин", "").strip())
        item['minRating'] = int(
            site.find_all("span", string=re.compile("Минимальный рейтинг для участия:"))[0].get_text().split(":")[
                1].strip())
        item['image'] = site.find_all("img")[0]['src']
        item['views'] = int(site.find_all("span", string=re.compile("Просмотры:"))[0].get_text().split(":")[1].strip())
        item['rating'] = float(site.find_all("span", string=re.compile("Рейтинг:"))[0].get_text().split(":")[1].strip())

        return item

zip_path = 'zip_var_49.zip'

# Распаковка zip-архива
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('temp_folder')

items = []

# Проходим по всем файлам в распакованной папке
folder_path = 'temp_folder'
for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        result = handle_file(f'{folder_path}\{filename}')
        items.append(result)

# Удаляем временную папку с распакованными файлами
shutil.rmtree(folder_path)

items = sorted(items, key=lambda x: x['rating'], reverse=True)

filtered_items = []
for tournament in items:
    if tournament['views'] >= 95000:
        filtered_items.append(tournament)

num_stat = get_num_stat("views", items)
city_freq = get_freq("type", items)

write_to_json("result_all.json", items)
write_to_json("result_filtered.json", filtered_items)
write_to_json("result_num_stat.json", num_stat)
write_to_json("result_type_stat.json", city_freq)


