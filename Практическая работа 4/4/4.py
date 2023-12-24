import json
import msgpack
import sqlite3
import os
import csv


def write_to_file(filename, data):
    with open(filename, "w", encoding='utf-8') as r_json:
        r_json.write(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            )
        )


if os.path.exists('..\data3.db'):
    os.remove('..\data3.db')


def read_csv_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        data = [row for row in reader]
    return data


def read_text_file(file_path):
    updates = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        update = {}
        for line in lines:
            if line.startswith("name::"):
                update['name'] = line[len("name::"):].strip()
            elif line.startswith("method::"):
                update['method'] = line[len("method::"):].strip()
            elif line.startswith("param::"):
                update['param'] = line[len("param::"):].strip()
            elif line.strip() == "=====":
                updates.append(update)
                update = {}
    return updates


# обработка обновлений
def quantity_sub(cursor, conn, param, product_name):
    cursor.execute(
        """
        UPDATE products
        SET quantity = quantity - ?
        WHERE name = ?
    """,
        (param, product_name),
    )
    conn.commit()


def quantity_add(cursor, conn, param, product_name):
    cursor.execute(
        """
        UPDATE products
        SET quantity = quantity + ?
        WHERE name = ?
    """,
        (param, product_name),
    )
    conn.commit()


def price_abs(cursor, conn, param, product_name):
    cursor.execute(
        """
        UPDATE products
        SET price = price + ?
        WHERE name = ?
    """,
        (param, product_name),
    )
    conn.commit()


def price_percent(cursor, conn, param, product_name):
    cursor.execute(
        """
        UPDATE products
        SET price = price * ?
        WHERE name = ?
    """,
        (param, product_name),
    )
    conn.commit()


def available(cursor, conn, param, product_name):
    cursor.execute(
        """
        UPDATE products
        SET isAvailable = ?
        WHERE name = ?
    """,
        (param, product_name),
    )
    conn.commit()


def remove(cursor, conn, param, product_name):
    cursor.execute(
        """
        DELETE FROM products
        WHERE name = ?
    """,
        (product_name,),
    )
    conn.commit()


def apply_updates(conn, updates):
    cursor = conn.cursor()

    for update in updates:
        product_name = update['name']
        param = update['param']
        method = update['method']

        try:
            if method == "quantity_sub":
                quantity_sub(cursor, conn, param, product_name)
            if method == "quantity_add":
                quantity_add(cursor, conn, param, product_name)
            if method == "price_abs":
                price_abs(cursor, conn, param, product_name)
            if method == "price_percent":
                price_percent(cursor, conn, param, product_name)
            if method == "available":
                available(cursor, conn, param, product_name)
            if method == "remove":
                remove(cursor, conn, param, product_name)

            cursor.execute('UPDATE products SET counter = counter + 1 WHERE name = ?', (product_name,))
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")

    conn.commit()


def create_insert_db(conn, product_data):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL CHECK("price" >= 0),
            quantity INTEGER NOT NULL CHECK("quantity" >= 0),
            fromCity TEXT NOT NULL,
            isAvailable BOOLEAN NOT NULL,
            views INTEGER NOT NULL DEFAULT 0 CHECK("views" >= 0),
            counter INTEGER NOT NULL DEFAULT 0 CHECK("counter" >= 0)
        )
    ''')

    for product in product_data:
        if product['views'] is None:
            cursor.execute('''
                INSERT INTO products (name, price, quantity, fromCity, isAvailable, views)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                product['name'], product['price'], product['quantity'], product['category'], product['fromCity'],
                product['isAvailable']
            ))
        else:
            cursor.execute('''
                INSERT INTO products (name, price, quantity, fromCity, isAvailable, views)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                product['name'], product['price'], product['quantity'], product['fromCity'], product['isAvailable'],
                product['views']
            ))

    conn.commit()


product_data_file_path = 'task_4_var_49_product_data.csv'
update_data_file_path = 'task_4_var_49_update_data.text'

# Reading product data from CSV file
product_data = read_csv_file(product_data_file_path)
update_data = read_text_file(update_data_file_path)

conn = sqlite3.connect('..\data3.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

create_insert_db(conn, product_data)
apply_updates(conn, update_data)

# вывести топ-10 самых обновляемых товаров
top_updated_products = cursor.execute('''SELECT name, counter
        FROM products
        ORDER BY counter
        DESC LIMIT 10''').fetchall()

write_to_file("top_updated_products.json", [dict(row) for row in top_updated_products])

# проанализировать цены товаров, найдя (сумму, мин, макс, среднее) для каждой группы, а также количество товаров в группе
price_analysis_query = '''
    SELECT
        fromCity,
        SUM(price) AS total_price,
        MIN(price) AS min_price,
        MAX(price) AS max_price,
        AVG(price) AS avg_price,
        COUNT(*) AS product_count
    FROM products
    GROUP BY fromCity
'''
price_analysis_results = cursor.execute(price_analysis_query).fetchall()

results_list = []
for result in price_analysis_results:
    group_result = {
        "Group": result[0],
        "Total Price": result[1],
        "Min Price": result[2],
        "Max Price": result[3],
        "Avg Price": result[4],
        "Product Count": result[5]
    }
    results_list.append(group_result)

write_to_file("price_analysis.json", results_list)

# проанализировать остатки товаров, найдя (сумму, мин, макс, среднее) для каждой группы товаров
quantity_analysis_query = '''
    SELECT
        fromCity,
        SUM(quantity) AS total_quantity,
        MIN(quantity) AS min_quantity,
        MAX(quantity) AS max_quantity,
        AVG(quantity) AS avg_quantity,
        COUNT(*) AS product_count
    FROM products
    GROUP BY fromCity
'''
quantity_analysis_results = cursor.execute(quantity_analysis_query).fetchall()
json_data = []
for result in quantity_analysis_results:
    group_data = {
        "Group": result[0],
        "Total Quantity": result[1],
        "Min Quantity": result[2],
        "Max Quantity": result[3],
        "Avg Quantity": result[4],
        "Product Count": result[5],
    }
    json_data.append(group_data)

write_to_file("quantity_analysis.json", json_data)

# произвольный запрос
custom_query = '''
    SELECT
        p.fromCity,
        AVG(p.price)
    FROM products p
    JOIN (
        SELECT fromCity, AVG(quantity) AS avg_quantity
        FROM products
        GROUP BY fromCity
    ) AS avg_quantity_per_city
    ON p.fromCity = avg_quantity_per_city.fromCity
    WHERE p.quantity > avg_quantity_per_city.avg_quantity
    GROUP BY p.fromCity
'''
custom_query_result = cursor.execute(custom_query).fetchall()
output_data = [{"City": result[0], "Average_Price": result[1]} for result in custom_query_result]
write_to_file("custom_query.json", output_data)

conn.close()