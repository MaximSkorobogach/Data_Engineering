#https://www.kaggle.com/datasets/andreinovikov/air-pollution
import pandas as pd
from pymongo import MongoClient
from bson import json_util
import json

# Подключение к MongoDB
client = MongoClient()
db = client['health_data']
collection_air_pollution = db['air_pollution_data']
collection_dog = db['dog_data']

# Загрузка и вставка данных об уровне загрязнения воздуха
air_pollution_data = pd.read_csv('air_pollution.csv')
air_pollution_data = air_pollution_data.to_dict(orient='records')
collection_air_pollution.insert_many(air_pollution_data)

# Загрузка данных о собаках из JSON
with open('dog_dataset.json', 'r') as file:
    dog_data = json.load(file)

collection_dog.insert_many(dog_data)

# Примеры запросов и операций
# Запрос 1 - выборка данных
query_1_air_pollution = list(collection_air_pollution.find({"city": "Kabul"}))
query_1_dog = list(collection_dog.find({"age": 10, "height_cm": 100, "health_score": {"$gt": 9}}))

# Запрос 2 - выборка с агрегацией (пример)
query_2_air_pollution = list(collection_air_pollution.aggregate([
    {"$group": {"_id": "$country", "average_pollution_2021": {"$avg": "$2021"}}}
]))

# Обновление данных в коллекции загрязнения воздуха
collection_air_pollution.update_many({"city": "Algiers"}, {"$set": {"2022": 18.0}})

# Удаление данных на основе условия
collection_dog.delete_many({"weight_kg": {"$lt": 30}})

# Группировка данных
query_5_air_pollution = list(collection_air_pollution.aggregate([
    {"$group": {"_id": "$country", "total_cities": {"$sum": 1}}}
]))

# Примеры запросов
query_6_air_pollution = list(collection_air_pollution.find({"country": "Argentina"}).limit(3))

# Запрос 7 - выборка с агрегацией (пример)
query_7_air_pollution = list(collection_air_pollution.aggregate([
    {"$group": {"_id": "$country", "max_pollution_2021": {"$max": "$2021"}}},
    {"$sort": {"max_pollution_2021": -1}},
    {"$limit": 2}
]))

# Обновление данных в коллекции собак
collection_dog.update_many({"litter_size": {"$gte": 10}}, {"$set": {"health_score": 10}})

# Удаление данных на основе условия
collection_air_pollution.delete_many({"2023": {"$lt": 10}})

# Группировка данных
query_10_air_pollution = list(collection_air_pollution.aggregate([
    {"$group": {"_id": "$country", "average_pollution": {"$avg": "$2022"}}}
]))

# Новые запросы для собак
# Запрос 2 - выборка с агрегацией (пример)
query_2_dog = list(collection_dog.aggregate([
    {"$group": {"_id": "$is_male", "average_weight": {"$avg": "$weight_kg"}}}
]))

# Удаление данных на основе условия (пример)
collection_dog.delete_many({"exercise_hours": {"$lt": 3}})

# Группировка данных (пример)
query_5_dog = list(collection_dog.aggregate([
    {"$group": {"_id": "$vaccinated", "total_entries": {"$sum": 1}}}
]))

# Примеры запросов
query_6_dog = list(collection_dog.find({"is_male": True}).limit(3))

# Запрос 7 - выборка с агрегацией (пример)
query_7_dog = list(collection_dog.aggregate([
    {"$group": {"_id": "$feeding_frequency", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 2}
]))

# Группировка данных (пример)
query_10_dog = list(collection_dog.aggregate([
    {"$group": {"_id": "$vaccinated", "average_health_score": {"$avg": "$health_score"}}}
]))

# Сохранение результатов в словаре
results = {
    "Query 1 Air Pollution": json.loads(json_util.dumps(query_1_air_pollution)),
    "Query 1 Dog": json.loads(json_util.dumps(query_1_dog)),
    "Query 2 Air Pollution": json.loads(json_util.dumps(query_2_air_pollution)),
    "Query 2 Dog": json.loads(json_util.dumps(query_2_dog)),
    "Query 5 Air Pollution": json.loads(json_util.dumps(query_5_air_pollution)),
    "Query 5 Dog": json.loads(json_util.dumps(query_5_dog)),
    "Query 6 Air Pollution": json.loads(json_util.dumps(query_6_air_pollution)),
    "Query 6 Dog": json.loads(json_util.dumps(query_6_dog)),
    "Query 7 Air Pollution": json.loads(json_util.dumps(query_7_air_pollution)),
    "Query 7 Dog": json.loads(json_util.dumps(query_7_dog)),
    "Query 10 Air Pollution": json.loads(json_util.dumps(query_10_air_pollution)),
    "Query 10 Dog": json.loads(json_util.dumps(query_10_dog)),
}

# Сохранение результатов в JSON-файл
with open('query_results.json', 'w') as json_file:
    json.dump(results, json_file, indent=2)

# Закрытие соединения с MongoDB
client.close()
