import sqlite3
import csv
import json
import os


# Предметная область - база данных о собаках
# dogs.csv - Родительская таблица о собаках (уникальный айди, порода, имя)
# dogs_ages - Данные о возрасте собаки (родительский айди, возраст) связывается с родительской по внешнему ключу ParentID = ID
# dogs_colors.json - Данные о цвете собаки (родительский айди, цвет собаки) связывается с родительской по внешнему ключу ParentID = ID

if os.path.exists('..\dog_database.db'):
    os.remove('..\dog_database.db')

conn = sqlite3.connect('..\dog_database.db')
cursor = conn.cursor()

# Создаем таблицу Dogs
cursor.execute('''CREATE TABLE IF NOT EXISTS Dogs (
                    ID INTEGER PRIMARY KEY,
                    Breed TEXT,
                    Name TEXT
                )''')

with open('dogs.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    next(csv_reader)
    for row in csv_reader:
        cursor.execute('INSERT INTO Dogs (ID, Breed, Name) VALUES (?, ?, ?)', (row[0], row[1], row[2]))

# Создаем таблицу DogAges
cursor.execute('''CREATE TABLE IF NOT EXISTS DogAges (
                    ID INTEGER PRIMARY KEY,
                    Age INTEGER,
                    ParentID INTEGER,
                    FOREIGN KEY (ParentID) REFERENCES Dogs (ID)
                )''')

with open('dogs_ages.json', 'r') as json_file:
    dog_age_data = json.load(json_file)
    for record in dog_age_data:
        cursor.execute('INSERT INTO DogAges (ParentID, Age) VALUES (?, ?)', (record['ParentID'], record['Age']))

# Создаем таблицу DogColors
cursor.execute('''CREATE TABLE IF NOT EXISTS DogColors (
                    ID INTEGER PRIMARY KEY,
                    Color TEXT,
                    ParentID INTEGER,
                    FOREIGN KEY (ParentID) REFERENCES Dogs (ID)
                )''')

with open('dogs_colors.json', 'r') as json_file:
    dog_color_data = json.load(json_file)
    for record in dog_color_data:
        cursor.execute('INSERT INTO DogColors (ParentID, Color) VALUES (?, ?)', (record['ParentID'], record['Color']))

conn.commit()

# Запрос 1: Выборка с простым условием + сортировка + ограничение количество
cursor.execute('''SELECT * FROM Dogs 
                  WHERE Breed = 'Rottweiler'
                  ORDER BY Name
                  LIMIT 5''')
result1 = cursor.fetchall()

# Запрос 2: Подсчет объектов по условию
cursor.execute('''SELECT COUNT(*) FROM DogAges
                  WHERE Age > 5''')
result2 = cursor.fetchall()

# Запрос 3: Группировка и подсчет среднего возраста для каждой породы
cursor.execute('''SELECT Dogs.Breed, AVG(DogAges.Age) AS AvgAge
                  FROM Dogs
                  JOIN DogAges ON Dogs.ID = DogAges.ParentID
                  GROUP BY Dogs.Breed''')
result3 = cursor.fetchall()

# Запрос 4: Обновление данных - увеличение возраста на 1 год для всех собак цвета "Black"
cursor.execute('''UPDATE DogAges
                  SET Age = Age + 1
                  WHERE ParentID IN (SELECT ID FROM DogColors WHERE Color = 'Black')''')

# Запрос 5: Выборка данных после обновления
cursor.execute('''SELECT * FROM DogAges
                  JOIN Dogs ON Dogs.ID = DogAges.ParentID
                  WHERE ParentID IN (SELECT ID FROM DogColors WHERE Color = 'Black')''')
result5 = cursor.fetchall()

# Запрос 6: Подсчет суммарного возраста для каждой породы
cursor.execute('''SELECT Dogs.Breed, SUM(DogAges.Age) AS TotalAge
                  FROM Dogs
                  JOIN DogAges ON Dogs.ID = DogAges.ParentID
                  GROUP BY Dogs.Breed''')
result6 = cursor.fetchall()

# Запрос 7: Найти три самых распространенных цвета шерсти для определенной породы
cursor.execute('''SELECT DogColors.Color, COUNT(DogColors.ID) AS ColorCount
                  FROM DogColors
                  JOIN Dogs ON DogColors.ParentID = Dogs.ID
                  WHERE Dogs.Breed = 'Golden Retriever'
                  GROUP BY DogColors.Color
                  ORDER BY ColorCount DESC
                  LIMIT 3''')
result7 = cursor.fetchall()

with open('result1_dogs.json', 'w') as json_file:
    json.dump(result1, json_file)

with open('result2_dogs.json', 'w') as json_file:
    json.dump(result2, json_file)

with open('result3_dogs.json', 'w') as json_file:
    json.dump(result3, json_file)

with open('result5_dogs.json', 'w') as json_file:
    json.dump(result5, json_file)

with open('result6_dogs.json', 'w') as json_file:
    json.dump(result6, json_file)

with open('result7_dogs.json', 'w') as json_file:
    json.dump(result7, json_file)

conn.close()
