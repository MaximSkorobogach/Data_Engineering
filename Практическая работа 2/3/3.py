import json
import msgpack
import statistics

with open('products_49.json', 'r') as json_file:
    data = json.load(json_file)

aggregated_data = {}

for item in data:
    name = item['name']
    price = item['price']

    if name not in aggregated_data:
        aggregated_data[name] = []

    aggregated_data[name].append(price)

for name, prices in aggregated_data.items():
    average_price = statistics.mean(prices)
    max_price = max(prices)
    min_price = min(prices)

    aggregated_data[name] = {
        "average_price": average_price,
        "max_price": max_price,
        "min_price": min_price
    }

with open('aggregated_data.json', 'w') as json_output_file:
    json.dump(aggregated_data, json_output_file)

with open('aggregated_data.msgpack', 'wb') as msgpack_output_file:
    packed_data = msgpack.packb(aggregated_data)
    msgpack_output_file.write(packed_data)

import os

json_file_size = os.path.getsize('aggregated_data.json')
msgpack_file_size = os.path.getsize('aggregated_data.msgpack')

print(f'Размер JSON: {json_file_size} байт')
print(f'Размер msgpack file: {msgpack_file_size} байт')