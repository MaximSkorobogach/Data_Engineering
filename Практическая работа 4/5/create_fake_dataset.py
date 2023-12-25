import csv
import json
import random

# Генерация случайных пород собак
dog_breeds = ["Labrador Retriever", "German Shepherd", "Golden Retriever", "Bulldog", "Beagle", "Poodle", "Rottweiler", "Siberian Husky", "Dachshund", "Shih Tzu"]

# Популярные имена для собак
dog_names = ["Bella", "Max", "Lucy", "Charlie", "Cooper", "Bailey", "Daisy", "Sadie", "Lola", "Tucker"]

dogs_count = 1000000
# Создание CSV файла
csv_file_path = 'dogs.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';')
    csv_writer.writerow(['ID', 'Breed', 'Name'])

    for i in range(dogs_count):
        breed = random.choice(dog_breeds)
        name = random.choice(dog_names)
        csv_writer.writerow([i + 1, breed, name])

# Чтение данных из CSV файла
csv_file_path = 'dogs.csv'
dog_data = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    for row in csv_reader:
        dog_data.append(row)

# Создание JSON файла 1 (dogs_colors.json)
json_file_path_colors = 'dogs_colors.json'
data_json_colors = [{'ParentID': int(entry['ID']), 'Color': random.choice(['Black', 'Brown', 'White', 'Spotted'])} for entry in dog_data]
with open(json_file_path_colors, 'w') as json_file_colors:
    json.dump(data_json_colors, json_file_colors, indent=2)

# Создание JSON файла 2 (dogs_ages.json)
json_file_path_ages = 'dogs_ages.json'
data_json_ages = [{'ParentID': int(entry['ID']), 'Age': random.randint(1, 10)} for entry in dog_data]
with open(json_file_path_ages, 'w') as json_file_ages:
    json.dump(data_json_ages, json_file_ages, indent=2)



