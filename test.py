# Путь к CSV-файлу
csv_file_path = 'data.csv'

# Создание датасета из CSV-файла
raw_data = tf.data.experimental.make_csv_dataset(
    csv_file_path,
    batch_size=batch_size,
    num_epochs=1,  # Количество эпох, по умолчанию 1
    shuffle=True,  # Перемешивать ли данные
    shuffle_buffer_size=10000,  # Размер буфера для перемешивания
    label_name='output_column_name'  # Имя столбца, который будет выходным
)

# Преобразование датасета
def preprocess_data(features, labels):
    # Переносим второй столбец входными данными
    inputs = features['input_column_name']
    # В первом столбце у вас, предположим, находятся метки, которые станут выходными данными
    outputs = labels
    return inputs, outputs

# Применяем преобразование к датасету
dataset = raw_data.map(preprocess_data)

# Пример чтения данных из датасета
for input_batch, output_batch in dataset.take(1):  # Пример извлечения одного батча данных
    print("Input batch:", input_batch)
    print("Output batch:", output_batch)