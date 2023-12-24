import sqlite3
import msgpack
import json


def write_to_file(filename, data):
    with open(filename, "w", encoding='utf-8') as r_json:
        r_json.write(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            )
        )


with open('task_1_var_49_item.msgpack', 'rb') as file:
    data = msgpack.load(file)

conn = sqlite3.connect('../data.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

create_table_query = '''
    CREATE TABLE "books" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "title" TEXT,
        "author" TEXT,
        "genre" TEXT,
        "pages" INTEGER,
        "published_year" INTEGER,
        "isbn" TEXT,
        "rating" REAL,
        "views" INTEGER
    );
'''
cursor.execute(create_table_query)

data_as_tuples = [(item["title"], item["author"], item["genre"], item["pages"], item["published_year"], item["isbn"],
                   item["rating"], item["views"]) for item in data]

cursor.executemany('''
    INSERT INTO books ("title", "author", "genre", "pages", "published_year", "isbn", "rating", "views")
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', data_as_tuples)

conn.commit()

# Запрос 1: Вывод первых (VAR+10) отсортированных по произвольному числовому полю строк из таблицы в файл формата json
var_value = 49
cursor.execute(f'SELECT * FROM books ORDER BY rating LIMIT ?', ((var_value + 10),))
result_1 = cursor.fetchall()

result_1 = [dict(row) for row in result_1]

write_to_file('output_1.json', result_1)

# Запрос 2: Вывод (сумму, мин, макс, среднее) по произвольному числовому полю
query = f'SELECT SUM(pages), MIN(pages), MAX(pages), AVG(pages) FROM books'
cursor.execute(query)
result_2 = cursor.fetchone()

result_2_dict = {
    'Sum': result_2[0],
    'Min': result_2[1],
    'Max': result_2[2],
    'Average': result_2[3]
}

write_to_file('output_2.json', result_2_dict)

# Запрос 3: Вывод частоты встречаемости для категориального поля
cursor.execute(f'SELECT genre, COUNT(*) as count FROM books GROUP BY genre')
result_3 = cursor.fetchall()
result_3 = [dict(row) for row in result_3]

write_to_file('output_3.json', result_3)

# Запрос 4: Вывод первых (VAR+10) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json
var_predicate = 2015
cursor.execute(f'SELECT * FROM books WHERE published_year > ? ORDER BY rating LIMIT ?',
               (var_predicate, var_value + 10,))
result_4 = cursor.fetchall()

result_4 = [dict(row) for row in result_4]

write_to_file('output_4.json', result_4)

conn.close()