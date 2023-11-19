import csv

def process_csv(input_file_path, output_file_path):
    records = []

    # Создание записей
    with open(input_file_path, newline="\n", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            record = {
                "number": int(row[0]),
                "full_name": row[2] + ' ' + row[1],
                "age": int(row[3]),
                "salary": int(row[4][0:-1])
            }

            records.append(record)

    average_salary = calculate_average_salary(records)

    filtered_records = filter_records(records, average_salary)

    sorted_records = sort_records(filtered_records)

    write_to_csv(output_file_path, sorted_records)

# Расчет среднего по зарплате
def calculate_average_salary(records):
    total_salary = sum(record["salary"] for record in records)
    return total_salary / len(records) if len(records) > 0 else 0

# Фильтрация записей
def filter_records(records, average_salary):
    return [
        record for record in records
        # Фильтруем записи по 25 + (номер варианта mod 10)
        if record["salary"] > average_salary and record["age"] > 25 + (49 % 10)
    ]

# Сортировка записей по номеру
def sort_records(records):
    return sorted(records, key=lambda record: record["number"])

# Внести записи в файл формата csv
def write_to_csv(output_file_path, records):
    with open(output_file_path, 'w', encoding="utf-8-sig", newline='') as file:
        writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for record in records:
            record["salary"] = str(record["salary"]) + "₽"
            writer.writerow(record.values())

process_csv('text_4_var_49', 'text_4_var_49_result')
