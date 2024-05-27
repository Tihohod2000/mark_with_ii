import psycopg2
from psycopg2 import OperationalError

# # Установить соединение с базой данных
# connection = psycopg2.connect(
#     user="postgres",
#     password="12345",
#     host="localhost",
#     port="5432",
#     database="diplom"
# )
#
# cursor = connection.cursor()
#
# # Пример выполнения INSERT-запроса
# insert_query = """INSERT INTO info (id, name) VALUES (%s, %s);"""
# record_to_insert = ('1', 'ДГТУ')
# cursor.execute(insert_query, record_to_insert)
# connection.commit()  # Фиксация изменений
#
# print("Запись успешно вставлена.")
#
# # Пример выполнения SELECT-запроса
# select_query = "SELECT * FROM info;"
# cursor.execute(select_query)
# records = cursor.fetchall()
#
# print("Результаты SELECT-запроса:")
# for row in records:
#     print(row)

def create_connection():
    try:
        # Установить соединение с базой данных
        connection = psycopg2.connect(
            user="postgres",
            password="12345",
            host="localhost",
            port="5432",
            database="diplom"
        )

        # cursor = connection.cursor()
        connection.set_client_encoding('UTF8')
        return connection

        # # Пример выполнения SELECT-запроса
        # select_query = "SELECT * FROM info;"
        # cursor.execute(select_query)
        # records = cursor.fetchall()
        #
        # print("Результаты SELECT-запроса:")
        # for row in records:
        #     print(row)

        # # Пример выполнения INSERT-запроса
        # insert_query = """INSERT INTO info (колонка1, колонка2) VALUES (%s, %s);"""
        # record_to_insert = ('значение1', 'значение2')
        # cursor.execute(insert_query, record_to_insert)
        # connection.commit()  # Фиксация изменений

        # print("Запись успешно вставлена.")

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    # finally:
    #     # Закрытие соединения
    #     if connection:
    #         cursor.close()
    #         connection.close()
    #         print("Соединение с PostgreSQL закрыто")
