import sys
import main_func
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt6 import uic
import psycopg2
import db_conn
import datetime
import csv


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)  # Загружает .ui файл напрямую

        self.pushButton_2.clicked.connect(self.handle_button_click)
        self.pushButton.clicked.connect(self.handle_button_click_2)
        self.pushButton_3.clicked.connect(self.export_to_csv)

    def handle_button_click(self):
        self.pushButton.setEnabled(False)
        # Получаем текст из textEdit и textEdit_2
        text1 = self.textEdit.toPlainText()
        text2 = self.textEdit_2.toPlainText()
        print("Text from textEdit:", text1)
        print("Text from textEdit_2:", text2)

        if text1 == "" or text1 == " ":
            QMessageBox.question(self, 'Ошибка', 'Произошла ошибка! Вы не ввели данные',
                                 QMessageBox.StandardButton.Ok)
            return

        global id_of_company
        global mark_of_map
        global right_name
        global right_category
        global right_address

        try:
            right_name, right_category, right_address, id_of_company, mark_of_map = main_func.open_drive(
                text1 + ' ' + text2)

            mark_of_map = str(mark_of_map.replace(".", ","))

            self.status.setText(
                f'Имя организации: {right_name}\nТип организации: {right_category}\nАдресс: {right_address}')
            self.pushButton.setEnabled(True)
        except Exception as e:
            self.status.setText(
                f'Произошла ошибка во время поиска организации: {e}')
            QMessageBox.question(self, 'Ошибка', 'Произошла ошибка во время поиска организации',
                                 QMessageBox.StandardButton.Ok)

    def handle_button_click_2(self):

        connection = db_conn.create_connection()
        if connection is not None:

            try:
                cursor = connection.cursor()
                # Пример выполнения SELECT-запроса
                select_query = f"SELECT * FROM info WHERE id_of_map = '{id_of_company}';"
                cursor.execute(select_query)
                records = cursor.fetchall()
                time_difference = 9999

                time_now = datetime.date.today()
                if len(records) > 0:
                    old_time = records[0][3]
                    time_difference = (time_now - old_time).days

                if len(records) > 0 and time_difference < 5:
                    print("Найдена запись")
                    print(records)
                    self.mark.setText(f'Оценка искусственного интелекта: {records[0][6]}')
                    if connection:
                        cursor.close()
                        connection.close()
                        print("Соединение с PostgreSQL закрыто")
                    QMessageBox.question(self, 'Уведомление', 'Данные были получены из базы данных',
                                         QMessageBox.StandardButton.Ok)
                    return

                else:

                    try:
                        mark_1, mark_2 = main_func.predict(id_of_company)
                        mark_1 = str(mark_1).replace('.', ',')
                        mark_2 = str(mark_2).replace('.', ',')
                    except Exception:
                        QMessageBox.question(self, 'Ошибка', 'Произошла ошибка во время получения отзывов',
                                             QMessageBox.StandardButton.Ok)
                        return

                    if mark_1 == 0 or mark_2 == 0:
                        self.mark.setText(f'Нет отзывов на картах')
                        if connection:
                            cursor.close()
                            connection.close()
                            print("Соединение с PostgreSQL закрыто")
                    else:
                        # Пример выполнения INSERT-запроса (если требуется)
                        if len(records) > 0:
                            insert_query = (
                                f"UPDATE info SET mark_of_map = '{mark_of_map}', net_mark = '{mark_1}', date = CURRENT_TIMESTAMP WHERE id_of_map = '{id_of_company}';")
                        else:
                            insert_query = (
                                f"INSERT INTO info (name, info, mark_of_map, net_mark, id_of_map, date, address) VALUES "
                                f"('{right_name}', '{right_category}', '{mark_of_map}', '{mark_1}', '{id_of_company}', CURRENT_TIMESTAMP, '{right_address}');")
                        cursor.execute(insert_query)
                        connection.commit()  # Фиксация изменений
                        print("Запись успешно вставлена.")
                        self.mark.setText(
                            f'Оценка искусственного интелекта: {mark_1}')
                        QMessageBox.question(self, 'Уведомление',
                                             'Все операции выполнены успешно. Оценка была произведена на свежих данных',
                                             QMessageBox.StandardButton.Ok)

                        if connection:
                            cursor.close()
                            connection.close()
                            print("Соединение с PostgreSQL закрыто")

                    # Для демонстрации выводим текст в консоль
                    print("Text from textEdit:", mark_1)
                    print("Text from textEdit_2:", mark_2)
            except UnicodeDecodeError as e:
                print(f"Ошибка декодирования: {e}")
                QMessageBox.question(self, 'Ошибка', 'Произошла ошибка во время работы с базой данных',
                                     QMessageBox.StandardButton.Ok)

        else:
            # Получаем текст из textEdit и textEdit_2

            try:
                mark_1, mark_2 = main_func.predict(id_of_company)
            except Exception:
                QMessageBox.question(self, 'Ошибка', 'Произошла ошибка во время получения отзывов',
                                     QMessageBox.StandardButton.Ok)
                return

            if mark_1 == 0 or mark_2 == 0:
                self.mark.setText(f'Нет отзывов на картах')
            else:
                self.mark.setText(f'Оценка искусственного интелекта: {mark_1}')

            # Для демонстрации выводим текст в консоль
            print("Text from textEdit:", mark_1)
            print("Text from textEdit_2:", mark_2)

        QMessageBox.question(self, 'Уведомление', 'Все операции выполнены успешно',
                             QMessageBox.StandardButton.Ok)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход', 'Вы действительно хотите выйти?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            print("Окно закрывается. Выполнение нужных действий...")
            main_func.discon()
            event.accept()
        else:
            event.ignore()

    def export_to_csv(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "CSV Files (*.csv);;All Files (*)")
        if fileName:
            self.save_data_to_csv(fileName)

    def save_data_to_csv(self, output_file):
        try:
            connection = db_conn.create_connection()
            if connection is not None:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM info")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                with open(output_file, 'w', newline='', encoding='cp1251') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=';')
                    csvwriter.writerow(columns)
                    csvwriter.writerows(rows)
                print(f"Данные успешно сохранены в файл {output_file}")
            else:
                print("Не удалось подключиться к базе данных")
                QMessageBox.question(self, 'Ошибка', 'Произошла ошибка при при подключении к БД',
                                     QMessageBox.StandardButton.Ok)
        except (Exception, psycopg2.Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            QMessageBox.question(self, 'Ошибка', 'Произошла ошибка при сохранении данных в csv файл',
                                 QMessageBox.StandardButton.Ok)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
