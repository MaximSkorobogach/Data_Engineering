import sqlite3
import os
import pickle
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

if os.path.exists('..\data2.db'):
    os.remove('..\data2.db')

conn = sqlite3.connect('..\data2.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE "songs" (
    "Id" INTEGER,
    "artist" TEXT,
    "song" TEXT,
    "duration_ms" INTEGER,
    "year" INTEGER,
    "tempo" REAL,
    "genre" TEXT,
    PRIMARY KEY("Id" AUTOINCREMENT)
);
'''
cursor.execute(create_table_query)
conn.commit()

pickle_file_path = 'task_3_var_49_part_1.pkl'

with open(pickle_file_path, 'rb') as pickle_file:
    pickle_data = pickle.load(pickle_file)

    data_to_insert = [
        (
            row['artist'],
            row['song'],
            row['duration_ms'],
            row['year'],
            row['tempo'],
            row['genre']
        ) for row in pickle_data
    ]

if data_to_insert:
    cursor.executemany('''
        INSERT INTO songs (artist, song, duration_ms, year, tempo, genre)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data_to_insert)

json_file_path = 'task_3_var_49_part_2.json'

with open(json_file_path, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

    data_to_insert = [
        (
            row['artist'],
            row['song'],
            row['duration_ms'],
            row['year'],
            row['tempo'],
            row['genre']
        ) for row in json_data
    ]

if data_to_insert:
    cursor.executemany('''
        INSERT INTO songs (artist, song, duration_ms, year, tempo, genre)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data_to_insert)

conn.commit()

# вывод первых (VAR+10) отсортированных по произвольному числовому полю строк из таблицы в файл формата json;
select_query = '''
    SELECT * FROM songs
    ORDER BY duration_ms
    LIMIT ?
'''

var = 49
cursor.execute(select_query, (var + 10,))
result_rows = cursor.fetchall()

result_rows = [dict(row) for row in result_rows]

json_file_path = 'sorted_data.json'
write_to_file(json_file_path, result_rows)

# вывод (сумму, мин, макс, среднее) по произвольному числовому полю;
stats_query = '''
    SELECT 
        SUM(duration_ms) as total_duration,
        MIN(duration_ms) as min_duration,
        MAX(duration_ms) as max_duration,
        AVG(duration_ms) as avg_duration
    FROM songs
'''

cursor.execute(stats_query)
stats_result = cursor.fetchone()

stats_data = {
    'Статистика по полю duration_ms': {
        'Total Duration': stats_result[0],
        'Min Duration': stats_result[1],
        'Max Duration': stats_result[2],
        'Average Duration': stats_result[3]
    }
}

write_to_file('stats.json', stats_data)

# вывод частоты встречаемости для категориального поля
frequency_query = '''
    SELECT year, COUNT(*) as frequency
    FROM songs
    GROUP BY year
    ORDER BY frequency DESC
'''

cursor.execute(frequency_query)
frequency_result = cursor.fetchall()

frequency_data = {'Частота по годам': {str(year): frequency for year, frequency in frequency_result}}
write_to_file('frequency.json', frequency_data)

# вывод первых (VAR+15) отфильтрованных по произвольному
# предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json.
filter_query = '''
    SELECT * FROM songs
    WHERE year > 2010
    ORDER BY duration_ms
    LIMIT ?
'''

cursor.execute(filter_query, (var + 15,))
filtered_result_rows = cursor.fetchall()

result_rows = [dict(row) for row in filtered_result_rows]

filtered_json_file_path = 'filtered_sorted_data.json'
write_to_file(filtered_json_file_path, result_rows)

conn.close()