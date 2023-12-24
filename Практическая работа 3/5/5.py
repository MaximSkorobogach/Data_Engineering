import json
from bs4 import BeautifulSoup
import os
import re
import numpy as np


def write_to_json(path: str, data: str):
    with open(path, 'w', encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False))

def get_num_stat(selector, items):
    nums = list(map(lambda x: float(x[selector]), items))

    stat = {}
    stat['sum'] = sum(nums)
    stat['min'] = min(nums)
    stat['max'] = max(nums)
    stat['avg'] = np.average(nums)
    stat['std'] = np.std(nums)

    return stat


# Function to get frequency of labels in a text field
def get_freq(selector, items):
    freq = {}

    for item in items:
        if selector in item:
            freq[item[selector]] = freq.get(item[selector], 0) + 1

    return freq

# Список для хранения результатов парсинга
parsed_results = []
folder_path = 'pages'


for filename in os.listdir(folder_path):
    if filename.endswith('.html'):

        file_path = os.path.join(folder_path, filename)

        #Создаем объект BeautifulSoup
        with open(file_path, 'r', encoding='utf-8') as file:
            html_code = file.read()
        soup = BeautifulSoup(html_code, 'html.parser')

        # Extracting data
        article = soup.find('div', {'class': 'style_article__H2ZPn'}).text.strip()
        product_name = soup.find('h1', {'data-testid': 'ProductTitle__title'}).text.strip()
        brand = soup.find('a', {'data-testid': 'brand-link'}).text.strip()
        bonus_value_text = soup.find('span', {'data-testid': 'Bonus__value'}).text
        bonus_value = re.findall(r'\d+', bonus_value_text)[0]
        product_weight_text = soup.find('div', {'class': 'style_tile_weight__wu-cI'}).text
        product_weight = re.findall(r'\d+', product_weight_text)[0]
        quantity_text = soup.find('input', {'data-testid': 'QuantityCounter__input'}).get('value')
        quantity = re.findall(r'\d+', quantity_text)[0]
        availability_text = soup.find('div', {'data-testid': 'deliveryInfo'}).text.strip()
        availability = availability_text.lower() == "в наличии"
        default_price_text = soup.find('div', {'data-testid': 'default-price'}).find('span',
                                                                                {'data-testid': 'Price__val'}).text
        default_price_text = re.findall(r'\d+', default_price_text)[0]
        smart_price = soup.find('div', {'data-testid': 'SmartPriceRow'}).find('span',
                                                                              {'data-testid': 'Price__val'}).text
        default_price = re.findall(r'\d+', default_price_text)[0]

        # Check if the element is found before trying to access its text attribute
        discount_element = soup.find('span', {'data-testid': 'PriceItem__discount'})
        discount_percent = discount_element.text.replace('%', '').replace(' ', '') if discount_element else None

        delivery_info = soup.find('div', {'class': 'style_button_express_desktop__A1EhH'}).find('div', {
            'class': 'ExpressLabels_label__XcQAv'}).text

    # Собираем результаты парсинга в словарь
    result = {
        'article': article,
        'product_name': product_name,
        'brand': brand,
        'bonus_value': bonus_value,
        'product_weight': product_weight,
        'quantity': quantity,
        'availability': availability,
        'default_price': default_price,
        'smart_price': smart_price,
        'discount_percent': discount_percent,
        'delivery_info': delivery_info,
    }

    # Добавляем результаты в список
    parsed_results.append(result)

# Записываем результаты в JSON-файл
with open('parsed_results.json', 'w', encoding='utf-8') as json_file:
    json.dump(parsed_results, json_file, ensure_ascii=False, indent=2)

with open('parsed_results.json', 'r', encoding='utf-8') as file:
    parsed_results = json.load(file)

items = []
for result in parsed_results:
    item = {
        "article": result["article"],
        "product_name": result["product_name"],
        "brand": result["brand"],
        "bonus_value": result["bonus_value"],
        "product_weight": result["product_weight"],
        "quantity": result["quantity"],
        "availability": result["availability"],
        "default_price": result["default_price"],
        "smart_price": result["smart_price"],
        "discount_percent": result["discount_percent"],
        "delivery_info": result["delivery_info"]
    }
    items.append(item)

sorted_items = sorted(items, key=lambda x: float(x['default_price']))

filtered_items = [item for item in items if int(item['bonus_value']) > 15]

num_stat_product_weight = get_num_stat("product_weight", items)

brand_freq = get_freq("brand", items)

write_to_json("result_sorted.json", sorted_items)
write_to_json("result_filtered_bonus.json", filtered_items)
write_to_json("result_num_stat_product_weight.json", num_stat_product_weight)
write_to_json("result_brand_freq.json", brand_freq)
