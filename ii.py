import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import tensorflow as tf
import csv
import os

from tensorflow.keras import layers
from tensorflow.keras import losses


# Путь к вашему CSV-файлу
csv_file = '/content/drive/MyDrive/dataset/dataset.csv'

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

    current_row = 0

    for row in reader:

        current_row += 1
        if current_row < 0:
            continue
        if current_row > 50:
            break

        rating = row[0]  # Рейтинг
        if (("rating" not in row[0])):
                continue
        rating = rating.replace("rating=","")  # Рейтинг
        rating = rating.replace(".","")  # Рейтинг
        text = row[1]    # Текст
        text = text.replace("text=", "")    # Текст
        # text = text.replace("\\n", " ")    # Текст

        folder_name = f'/content/dataset/train/{rating}'
        create_folder_if_not_exists(folder_name)
        file_number = next_file_number(folder_name)
        file_name = f'{folder_name}/{file_number}.txt'

        # create_folder_if_not_exists(folder_name)

        with open(file_name, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

print("Готово!")

# Путь к вашему CSV-файлу
csv_file = '/content/drive/MyDrive/dataset/dataset.csv'

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

    current_row = 0

    for row in reader:

        current_row += 1
        if current_row < 50:
            continue
        if current_row > 60:
            break

        rating = row[0]  # Рейтинг
        if (("rating" not in row[0])):
                continue
        rating = rating.replace("rating=","")  # Рейтинг
        rating = rating.replace(".","")  # Рейтинг
        text = row[1]    # Текст
        text = text.replace("text=", "")    # Текст
        # text = text.replace("\\n", " ")    # Текст

        folder_name = f'/content/dataset/test/{rating}'
        create_folder_if_not_exists(folder_name)
        file_number = next_file_number(folder_name)
        file_name = f'{folder_name}/{file_number}.txt'

        # create_folder_if_not_exists(folder_name)

        with open(file_name, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

print("Готово!")

dataset_dir = '/content/dataset'
os.listdir(dataset_dir)
train_dir = os.path.join(dataset_dir, 'train')
os.listdir(train_dir)
sample_file = os.path.join(train_dir, '5/1.txt')
with open(sample_file) as f:
  print(f.read())

# Создание списка меток классов
class_names = ['0', '1', '2', '3', '4', '5']

# Вывод меток классов
for i, class_name in enumerate(class_names):
    print(f"Метка для рейтинга {i} ==> {class_name}")
batch_size = 128
seed = 42
raw_train_ds = tf.keras.utils.text_dataset_from_directory(
    '/content/dataset/train',
    batch_size=batch_size,
    validation_split=0.2,
    subset='training',
    seed=seed)

for text_batch, label_batch in raw_train_ds.take(5):
    print("Text:", text_batch.numpy())
    print("Label:", label_batch.numpy())

raw_val_ds = tf.keras.utils.text_dataset_from_directory(
    '/content/dataset/train',
    batch_size=batch_size,
    validation_split=0.2,
    subset='validation',
    seed=seed)
raw_test_ds = tf.keras.utils.text_dataset_from_directory(
    '/content/dataset/test',
    batch_size=batch_size)

max_features = 1000
sequence_length = 128

vectorize_layer = layers.TextVectorization(
    # standardize=custom_standardization,
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length)

raw_train_ds_labels = raw_train_ds.map(lambda _, y: y)
labels_batch = next(iter(raw_train_ds_labels))
print("Форма меток батча (raw_train_ds):", la-bels_batch.shape)
print("Метки батча:", labels_batch)

train_text = raw_train_ds.map(lambda x, y: x)
vectorize_layer.adapt(train_text)

def vectorize_text(text, label):
  text = tf.expand_dims(text, -1)
  return vectorize_layer(text), label

# retrieve a batch (of 32 reviews and labels) from the da-taset
text_batch, label_batch = next(iter(raw_train_ds))
first_review, first_label = text_batch[0], label_batch[0]
print("Review", first_review)
print("Label", raw_train_ds.class_names[first_label])
print("Vectorized review", vectorize_text(first_review, first_label))

print("187 ---> ",vectorize_layer.get_vocabulary()[187])
print(" 313 ---> ",vectorize_layer.get_vocabulary()[313])
print('Vocabulary size: {}'.format(len(vectorize_layer.get_vocabulary())))

train_ds = raw_train_ds.map(vectorize_text)
val_ds = raw_val_ds.map(vectorize_text)
test_ds = raw_test_ds.map(vectorize_text)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

vocab_size = 10000  # Размер словаря
embedding_dim = 128  # Размерность пространства вложений

# Определение модели
model = tf.keras.Sequential([
    layers.Embedding(input_dim=vocab_size, out-put_dim=embedding_dim, input_length=None),
    layers.LSTM(units=128, return_sequences=False),# LSTM-слои с 128 нейронами
    layers.Dense(units=128, activation='sigmoid'),
    layers.Dropout(0.2),
    layers.Dense(units=86, activation='sigmoid'),
    layers.Dropout(0.2),
    layers.Dense(units=1, activation='relu')
    #layers.Dense(units=1, activation='relu')# Выходной слой с 1 нейронами
])
model.summary()

# Компиляция модели
model.compile(optimizer='adam', loss='mse', met-rics=['accuracy'])


# Обучение модели
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=5,
    batch_size=32,
    )

export_model = tf.keras.Sequential([
  vectorize_layer,
  model
])

export_model.compile(
    loss='mean_squared_error', optimizer="adam", met-rics=['accuracy']
)

# Test it with `raw_test_ds`, which yields raw strings
loss, accuracy = export_model.evaluate(raw_test_ds)
print(accuracy)

examples = [
  #5
  "Лучший шоп на крохалях Большоц ассортимент, хорошая атмо-сфера,\nГлавное добрые и отзывчивые продавцы Рекомендую этот вейп шоп",
  #2
  "Раньше было нормально и мыли хорошо. Но больше не езжу ту-да. Как-то занял очередь, а передо мной мойщик стал «своих» про-пускать без очереди. Ругаться с такими смысла нет и что-то требо-вать, они там все не русские, у них свои понятия ",
  #3
  "Московский квартал 2.\nШумно : летом по ночам дикие гонки. Грязно : кругом стройки, невозможно открыть окна (16 этаж! ), веч-но по району летает мусор. Детские площадки убогие, на большой площади однотипные конструкции. Очень дорогая коммуналка. Часто срабатывает пожарная сигнализация. Жильцы уже не реагируют. В это время, обычно около часа, не работают лифты. Из плюсов - отличная планировка квартир ( Московская 194 ), на мой взгляд. Ремонт от застройщика на 3-. Окна вообще жуть - вместо вентиляции. По соот-ношению цена/качество - 3.",
  #0
  "Нет растительного масла для салата, нет зубочисток на сто-лах. Номер требует ремонта: шкаф разваливается, дверь не закрыва-лась вызывали плотника, туалетная комната стеклянная полочка ото-рвана вызывали плотника починил, телевизор старый пульт разбит и не работает посуду для чая не не выдают (тарелки,ложки, кружки) даже за отдельную плату",
  #5
  "Очень вкусно! И по домашнему! Замечательный комплексный обед! Не дорого, порции хорошие! ",
  #3
  "Доступные цены, широкий выбор и свежая рыба. Часто устраи-вают акции и можно взять гигантские куски рыбы за очень низкую це-ну. Еще консультант такой приятный сегодня попался, все объяснила, рассказала и поделилась как сама готовить определенные куски рыбы, что было очень интересно ????\n\nUPD: попросила сегодня натураль-ную рыбу, сама конечно виновата, что не проверила, когда клали в пакет, а по итогу продали слабосоленую, испортив этим ужин и настроение. Видимо раз на раз сервис не приходится. ",
  #1
  "Заказали фо-бо и том-ям\nКороче больше не приду к ним. \nВ том яме заявлены черри их нет в том ям идет кокосовое молоко его нет. \nФо-бо воняет чем то не приятно. В фо-бо нет ростков пшени-цы, нет кинзы. Спрашивается почему цена как за целое блюдо, но в блюдах не хватает компонентов. Не позортесь. Смените название, на собрали из того что было Позор руководству производства. ",
  #0
  "Все довольны, и взрослые и дети.\nВкусная еда.\nБанька и бассейны всё замечательно.\nЕздием к вам уже 4 год и привозим к вам ещё новых гостей(делаем вам рекламу) ????номера комфортные, чистые и уютные.",
  #мой коммент
  "Расположено отделение в центре города в здании Дом Профсо-юзов, в шаговой доступности от остановки общественного транспорта. Вежливый персонал, но большим минус для меня стало соедующее: при оформлении дебетовой карты специалист сообщила,что без оформления страховки и оплаты по страховки карту получить нельзя. Я оплатила, дозвонилась на горячую линию и выяснила , что это нет так.Мне при-шлось вернуться в отделение и после бурного обсуждения мне оформи-ли возврат средств."
]
export_model.predict(examples)

export_model.save('/content/drive/MyDrive/ВКР/model_LSTM_2')

loaded_model = tf.keras.models.load_model('/content/drive/MyDrive/ВКР/model_LSTM_3')

loaded_model.predict(
