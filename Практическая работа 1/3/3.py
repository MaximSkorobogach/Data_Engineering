def process_file(file_path):
    # Создаем список для хранения обработанных строк
    processed_lines = []

    with open(file_path, 'r') as input_file:
        # Читаем каждую строку из файла
        for line in input_file:
            # Разбиваем строку на числа, используя запятую в качестве разделителя
            numbers = line.split(',')

            # Заменяем "NA" на среднее значение соседних чисел
            for i in range(len(numbers)):
                if numbers[i] == "NA":
                    # Вычисляем среднее значение соседних чисел, если они существуют
                    neighbors = [float(numbers[j]) for j in range(max(0, i - 1), min(len(numbers), i + 2)) if
                                 numbers[j] != "NA"]
                    if neighbors:
                        numbers[i] = str(sum(neighbors) / len(neighbors))
                    else:
                        # Если нет соседних чисел, заменяем "NA" на 0
                        numbers[i] = "0"

            # Фильтруем числа, исключив те, у которых корень квадратный меньше 50 + 49 вариант
            filtered_numbers = [num for num in numbers if float(num) ** 0.5 >= 99]

            # Преобразуем числа обратно в строку
            processed_line = ','.join(filtered_numbers)

            # Добавляем обработанную строку в список
            processed_lines.append(processed_line)

    # Записываем обработанные строки в выходной файл
    with open('text_3_var_49_result', 'w') as output_file:
        for processed_line in processed_lines:
            output_file.write(f'{processed_line}')


# Пример использования
process_file('text_3_var_49')
