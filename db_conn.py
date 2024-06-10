import psycopg2


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



    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    # finally:
    #     # Закрытие соединения
    #     if connection:
    #         cursor.close()
    #         connection.close()
    #         print("Соединение с PostgreSQL закрыто")
