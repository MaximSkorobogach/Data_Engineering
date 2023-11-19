from bs4 import BeautifulSoup
import csv

def extract_table_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Находим таблицу в HTML
    table = soup.find('table')

    # Инициализируем списки для заголовков и данных
    headers = []
    data = []

    # Извлекаем заголовки таблицы
    for th in table.find_all('th'):
        headers.append(th.text.strip())

    # Извлекаем данные из строк таблицы
    for row in table.find_all('tr')[1:]:
        row_data = [td.text.strip() for td in row.find_all('td')]
        data.append(row_data)

    return headers, data

def write_to_csv(headers, data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        writer.writerows(data)

def read_html_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

html_file_path = 'text_5_var_49'
html_content = read_html_from_file(html_file_path)

headers, data = extract_table_data(html_content)
write_to_csv(headers, data, 'text_5_var_49_result')
