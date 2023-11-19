def count_word_frequency(file_path):
    # Чтение файла
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Разделение текста на слова и подсчет частоты
    words = text.split()
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1

    # Сортировка по убыванию частоты
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Запись результатов в файл
    with open('text_1_var_49_result', 'w', encoding='utf-8') as result_file:
        for word, freq in sorted_word_counts:
            result_file.write(f'{word}:{freq}\n')

# Пример использования
count_word_frequency('text_1_var_49')
