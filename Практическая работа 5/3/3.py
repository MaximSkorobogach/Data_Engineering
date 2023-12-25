import pickle
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['mydatabase']

collection_name = 'mycollection'
collection = db[collection_name]

file_path_task_3 = 'task_3_item.pkl'

with open(file_path_task_3, 'rb') as file_task_3:
    data_task_3 = pickle.load(file_task_3)

collection.insert_many(data_task_3)

# 1
collection.delete_many({"$or": [{"salary": {"$lt": 25000}}, {"salary": {"$gt": 175000}}]})

# 2
collection.update_many({}, {"$inc": {"age": 1}})

# 3
selected_professions = ["Архитектор", "Водитель", "Продавец"]
collection.update_many({"profession": {"$in": selected_professions}},
                       {"$mul": {"salary": 1.05}})

# 4
selected_cities = ["Бургос", "Бильбао", "Краков"]
collection.update_many({"city": {"$in": selected_cities}},
                       {"$mul": {"salary": 1.07}})

# 5
complex_predicate_filter = {
    "city": "Махадаонда",
    "job": {"$in": ["Врач", "IT-специалист", "Медсестра"]},
    "age": {"$gte": 20, "$lte": 30}
}
collection.update_many(complex_predicate_filter, {"$mul": {"salary": 1.10}})


# 6
random_predicate_filter = {"job": "Программист"}
collection.delete_many(random_predicate_filter)

client.close()