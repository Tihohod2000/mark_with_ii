import csv
import os

# Путь к вашему CSV-файлу
csv_file = 'Книга1.csv'

# Создание папки, если её еще нет
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Функция для определения следующего доступного номера файла
def next_file_number(folder_path):
    files = os.listdir(folder_path)
    count_file = len(files)
    if count_file:
        return count_file + 1
    else:
        return 1

# Чтение CSV-файла и создание папок и файлов
with open(csv_file, 'r', encoding='cp1251') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Пропускаем заголовки
    for row in reader:
        rating = row[0]  # Рейтинг
        if (("rating" not in row[0])):
                continue
        rating = rating.replace("rating=","")  # Рейтинг
        rating = rating.replace(".","")  # Рейтинг
        text = row[1]    # Текст
        text = text.replace("text=", "")    # Текст
        # text = text.replace("\\n", " ")    # Текст

        folder_name = f'rating/{rating}'
        create_folder_if_not_exists(folder_name)
        file_number = next_file_number(folder_name)
        file_name = f'{folder_name}/{file_number}.txt'

        # create_folder_if_not_exists(folder_name)

        with open(file_name, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

print("Готово!")
