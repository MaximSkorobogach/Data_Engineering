def calculate_line_averages(file_path):
    # Создаем список для хранения средних значений по каждой строке
    averages = []

    with open(file_path, 'r') as input_file:
        # Читаем каждую строку из файла
        for line in input_file:
            # Разбиваем строку на числа, используя точку с запятой в качестве разделителя
            numbers = [int(num) for num in line.split(';')]
            # Считаем среднее арифметическое чисел в строке
            line_average = sum(numbers) / len(numbers)
            # Добавляем среднее в список
            averages.append(line_average)

    # Записываем средние значения по каждой строке в выходной файл
    with open('text_2_var_49_result', 'w') as output_file:
        for line_average in averages:
            output_file.write(f'{line_average}\n')

calculate_line_averages('text_2_var_49')
