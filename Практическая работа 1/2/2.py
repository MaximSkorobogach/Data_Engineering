def calculate_line_sums(file_path):
    # Создаем список для хранения сумм по каждой строке
    sums = []

    with open(file_path, 'r') as input_file:
        # Читаем каждую строку из файла
        for line in input_file:
            # Разбиваем строку на числа, используя точку с запятой в качестве разделителя
            numbers = [int(num) for num in line.split(';')]
            # Считаем сумму чисел в строке
            line_sum = sum(numbers)
            # Добавляем сумму в список
            sums.append(line_sum)

    # Записываем суммы по каждой строке в выходной файл
    with open('text_2_var_49_result', 'w') as output_file:
        for line_sum in sums:
            output_file.write(f'{line_sum}\n')

calculate_line_sums('text_2_var_49')
