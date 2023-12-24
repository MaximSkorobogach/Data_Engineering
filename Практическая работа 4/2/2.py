import sqlite3
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

conn = sqlite3.connect('..\data.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

create_table_query_2 = '''
    CREATE TABLE "book_sales" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "title" TEXT,
        "price" INTEGER,
        "place" TEXT,
        "date" TEXT,
        FOREIGN KEY ("title") REFERENCES "books" ("title")
    );
'''
cursor.execute(create_table_query_2)

with open('task_2_var_49_subitem.json', 'r', encoding='utf-8') as file:
    data_2 = json.load(file)

data_as_tuples = [(item["title"], item["price"], item["place"], item["date"]) for item in data_2]

cursor.executemany('''
        INSERT INTO book_sales ("title", "price", "place", "date")
        VALUES (?, ?, ?, ?)
    ''', data_as_tuples)

conn.commit()

# Запрос 1
cursor.execute('''
    SELECT books.title, books.author, book_sales.price
    FROM books
    JOIN book_sales ON books.title = book_sales.title
    WHERE book_sales.place = 'offline'
    LIMIT 10;
''')
result_1 = cursor.fetchall()
result_1 = [dict(row) for row in result_1]
write_to_file('output_1.json', result_1)

# Запрос 2
cursor.execute('''
    SELECT books.title, books.genre, book_sales.date, book_sales.price
    FROM books
    JOIN book_sales ON books.title = book_sales.title
    WHERE book_sales.price < 2000
    LIMIT 10;
''')
result_2 = cursor.fetchall()
result_2 = [dict(row) for row in result_2]
write_to_file('output_2.json', result_2)

# Запрос 3
cursor.execute('''
    SELECT books.title, AVG(book_sales.price)
    FROM books
    JOIN book_sales ON books.title = book_sales.title
    GROUP BY books.title
    LIMIT 10;
''')
result_3 = cursor.fetchall()
result_3 = [dict(row) for row in result_3]
write_to_file('output_3.json', result_3)

conn.close()