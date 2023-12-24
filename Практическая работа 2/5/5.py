import json
import pandas as pd
import numpy as np
import msgpack
import pickle
import os

# Чтение данных из файла
with open('dog_dataset.json', 'r') as file:
    data = json.load(file)

# Выбор полей для дальнейшей обработки
selected_fields = ["age", "weight_kg", "height_cm", "vaccinated", "is_male", "health_score", "exercise_hours", "feeding_frequency", "grooming_needs"]

# Создание DataFrame из выбранных полей
df = pd.DataFrame(data)[selected_fields]

# Рассчет характеристик для числовых полей
numeric_stats = df.describe().to_dict()

# Рассчет частоты встречаемости для текстового поля "feeding_frequency"
feeding_frequency_counts = df["feeding_frequency"].value_counts().to_dict()

# Сохранение результатов в JSON
result = {
    "numeric_stats": numeric_stats,
    "feeding_frequency_counts": feeding_frequency_counts
}

with open('result.json', 'w') as result_file:
    json.dump(result, result_file, indent=2)

# Сохранение DataFrame в различных форматах
df.to_csv('result.csv', index=False)
df.to_json('result_dataframe.json', orient='records', lines=True)

# Использование библиотеки msgpack для сохранения DataFrame
with open('result.msgpack', 'wb') as msgpack_file:
    packed_data = msgpack.packb(df.to_dict(orient='split'))
    msgpack_file.write(packed_data)

df.to_pickle('result.pkl')

# Сравнение размеров файлов в МБ
original_size_mb = os.path.getsize('dog_dataset.json') / (1024 * 1024)
json_size_mb = os.path.getsize('result.json') / (1024 * 1024)
csv_size_mb = os.path.getsize('result.csv') / (1024 * 1024)
json_dataframe_size_mb = os.path.getsize('result_dataframe.json') / (1024 * 1024)
msgpack_size_mb = os.path.getsize('result.msgpack') / (1024 * 1024)
pkl_size_mb = os.path.getsize('result.pkl') / (1024 * 1024)

print(f"Размер исходного файла: {original_size_mb:.2f} МБ")
print(f"Размер файла result.json: {json_size_mb:.2f} МБ")
print(f"Размер файла result.csv: {csv_size_mb:.2f} МБ")
print(f"Размер файла result_dataframe.json: {json_dataframe_size_mb:.2f} МБ")
print(f"Размер файла result.msgpack: {msgpack_size_mb:.2f} МБ")
print(f"Размер файла result.pkl: {pkl_size_mb:.2f} МБ")
