import psycopg2
from db_functions import *

database = input('Введите название БД: ')
user = input('Введите имя юзера, под чьим именем подключаетесь к БД: ')
password = input('Введите пароль: ')

if __name__== '__main__':

    conn = psycopg2.connect(database=database, user=user, password=password)

    with conn.cursor() as cur:
        cur.execute('''
            DROP TABLE if exists Client CASCADE;
            DROP TABLE if exists Client_Phone CASCADE;
            ''')

        # Вызов функции создания таблиц
        # tables = ['Client', 'Client_Phone']
        # create_tables(cur, tables)
        # print()

        # Вызов функции добавления клиента
        # add_client(cur, 'Amir', 'Sadaqa', 'asadaka@inbox.ru')
        # add_client(cur, 'Petr', 'Petrov', 'petrov@inbox.ru')
        # add_client(cur, 'Amir', 'Sadaqa', 'amir.sadaka92@gmail.com')
        # add_client(cur, 'Maxim', 'Gershman', 'gershman@gmail.com')
        # add_client(cur, 'Maxim', 'Gershman', 'gershmanop@gmail.com')
        # print()

        # Вызов функции добавления телефона для существующего клиента
        # add_phone(cur, 'asadaka@inbox.ru', '+79152507637')
        # add_phone(cur, 'amir.sadaka92@gmail.com', '')
        # add_phone(cur, 'petrov@inbox.ru', '+7945632188')
        # add_phone(cur, 'gershman@gmail.com', '+7945632144')
        # add_phone(cur, 'petrov@inbox.ru', '+11111111111')
        # print()

        # Вызов функции, обновляющей данные о клиенте
        # update_client(cur, 'first_name', 'Ammar', 'sadaka.amir@mail.ru')
        # update_client(cur, 'first_name', 'Ammar', 'asadaka@inbox.ru')
        # update_client(cur, 'email', 'sadaka.amir@mail.ru', 'asadaka@inbox.ru')
        # update_client(cur, 'email', 'asadaka@inbox.ru', 'sadaka.amir@mail.ru')
        # update_client(cur, 'last_name', 'Sadaka', 'asadaka@inbox.ru')
        # update_client(cur, 'email', 'asadaka@inbox.ru', 'petrov@inbox.ru')
        # update_client(cur, 'last_name', 'Petrenko', 'petrov@inbox.ru')
        # print()

        # Вызов функции, удаляющей номер телефона (номера телефонов) для клиента:
        # delete_phone(cur, None, 'petrov@inbox.ru', '+7945632188')
        # delete_phone(cur, None, 'petrov@inbox.ru', '+11111111111')
        # delete_phone(cur, None, 'petrov@inbox.ru', None)
        # delete_phone(cur, None, 'gershman@gmail.com', None)
        # delete_phone(cur, 1, None, '+7945632188')
        # delete_phone(cur, 1, 'asadaka@inbox.ru', '+79152507637')
        # print()

        # Вызов ф-ции, удаляющей клиента
        # delete_client(cur, None, 'asadaka@inbox.ru')
        # delete_client(cur, 2, None)
        # delete_client(cur, None, 'drake@inbox.ru')
        # delete_client(cur, 80, None)
        # print()

        # Вызов функции, позволяющей найти клиента
        # find_client(cur, None, None, None, '+79152507637')
        # find_client(cur, None, None, None, '+7945632188')
        # find_client(cur, None, None, None, '+70000000000')
        # find_client(cur, None, None, 'petrov@inbox.ru', None)
        # find_client(cur, None, None, 'petrovaf@inbox.ru', None)
        # find_client(cur, 'Ammar', 'Sadaka', None, None)
        # find_client(cur, 'Ammar', 'Sadaqa', None, None)
        # find_client(cur, 'Ammar', 'Sadaqa', 'asadaka@inbox.ru', None)
        # find_client(cur, 'Maxim', 'Gershman', None, None)
        # find_client(cur, 'Ammar', 'Sadaka', None, '+79152507637')
        # find_client(cur, 'Pavel', 'Petrov', 'gershman@gmail.com', None)
        # find_client(cur, 'Artem', 'Krasnov', 'krasnov@mail.ru', '+79152507637')

    conn.close()