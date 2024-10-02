from psycopg2 import errors

def create_tables(cursor, tables):
    """
    Создает таблицы в базе данных, если они не существуют.

    Аргументы:
    - cursor: объект курсора для выполнения SQL-запросов.
    - tables: список названий таблиц, которые необходимо создать. Поддерживаются 'Client' и 'Client_Phone'.
    """

    for table in tables:
        if table == 'Client':
            query = f"""
            CREATE TABLE if not exists {table}(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(60) NOT NULL,
                last_name VARCHAR(60),
                email VARCHAR(60) NOT NULL UNIQUE
                );
            """
            cursor.execute(query)
        elif table == 'Client_Phone':
            query = f"""
                    CREATE TABLE if not exists {table}(
                        id SERIAL PRIMARY KEY,
                        phone_number VARCHAR(60) UNIQUE,
                        client_id INTEGER references Client(id) on DELETE CASCADE
                        );
                    """
            cursor.execute(query)

def add_client(cursor, first_name, last_name, email):
    """
    Добавляет нового клиента в таблицу 'Client'.

    Аргументы:
    - cursor: объект курсора для выполнения SQL-запросов.
    - first_name: имя клиента.
    - last_name: фамилия клиента.
    - email: email клиента, уникальный для каждого.

    Исключения:
    - errors.UniqueViolation: возникает, если email уже существует в базе данных.
    """

    query = f"""
            INSERT INTO Client(first_name, last_name, email) VALUES(%s, %s, %s); 
            """
    try:
        cursor.execute(query, (first_name, last_name, email))
        cursor.connection.commit()
        print(f'Клиент {first_name} c email {email} успешно добавлен в БД')
    except errors.UniqueViolation:
        print(f'{email} уже существует БД, попробуйте добавиться с другими email')
        cursor.connection.rollback()

def get_client_id(cursor, email):
    """
    Возвращает ID клиента по его email.

    Аргументы:
    - cursor: объект курсора для выполнения SQL-запросов.
    - email: email клиента.

    Возвращает:
    - ID клиента, если найден; иначе None.
    """

    query = """
    SELECT id FROM Client WHERE email = %s;
    """
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print(f'Клиент с email {email} не найден')
        return None

def add_phone(cursor, email, phone_number):
    """
    Добавляет номер телефона для клиента с указанным email.

    Аргументы:
    - cursor: объект курсора для выполнения SQL-запросов.
    - email: email клиента для идентификации.
    - phone_number: номер телефона для добавления.

    Исключения:
    - errors.UniqueViolation: если номер телефона уже существует,
      вставка откатывается.
    """

    client_id = get_client_id(cursor, email)

    if client_id:
        if phone_number is not None and phone_number != '':
            query = """
            INSERT INTO Client_Phone(phone_number, client_id) VALUES(%s, %s);
            """
            try:
                cursor.execute(query, (phone_number, client_id))
                cursor.connection.commit()
                print(f'Для клиента {client_id} c email {email} добавлен номер телефона {phone_number}')
            except errors.UniqueViolation:
                cursor.connection.rollback()
                print(f'Номер телефона {phone_number} уже существует в БД. Попробуйте добавиться с другим номером телефона')
        else:
            print(f'Клиент {client_id} c email {email} не оставил номер телефона')

def update_client(cursor, changed_data, to_be_value, email):
    """
    Обновляет информацию о клиенте.

    Аргументы:
    - cursor: объект курсора для выполнения SQL-запросов.
    - changed_data: поле, которое необходимо изменить (например, 'email' или др.).
    - to_be_value: новое значение для изменения.
    - email: email клиента для идентификации.

    Исключения:
    - errors.UniqueViolation: если новый email уже существует,
      обновление откатывается.
    """

    client_id = get_client_id(cursor, email)

    if client_id:
        if changed_data == 'email':
            try:
                query = f"""
                UPDATE Client SET {changed_data}=%s WHERE id=%s
                """
                cursor.execute(query, (to_be_value, client_id))
                cursor.connection.commit()
                print(f'Для клиента {client_id} email успешно изменен на {to_be_value}')
            except errors.UniqueViolation:
                cursor.connection.rollback()
                print(f'email {to_be_value} уже существует в БД')
        else:
            query = f"""
            UPDATE Client SET {changed_data}=%s WHERE id=%s
            """
            cursor.execute(query, (to_be_value, client_id))
            cursor.connection.commit()
            print(f'Для клиента {client_id} {changed_data} успешно изменен на {to_be_value}')

def delete_phone(cursor, id, email, phone_number=None):
    """
    Удаляет номер телефона для клиента.

    Аргументы:
    - cursor: объект курсора для выполнения SQL-запросов.
    - id: ID клиента (если известен).
    - email: email клиента (если ID не указан).
    - phone_number: конкретный номер телефона для удаления (если не указан, удаляются все номера).

    Исключения:
    - В случае отсутствия номера или клиента, удаление откатывается.
    """

    if id is None:
        client_id = get_client_id(cursor, email)
    else:
        client_id = id

    if client_id:
        if phone_number:
            query = f"""
            DELETE from Client_phone WHERE client_id=%s and phone_number=%s;
            """
            cursor.execute(query, (client_id, phone_number))
            if cursor.rowcount == 0:
                cursor.connection.rollback()
                print(f'Номер телефона {phone_number} не найден для клиента {client_id}')
            else:
                cursor.connection.commit()
                print(f'Номер телефона {phone_number} удален для клиента {client_id}')
        else:
            query = f"""
                    DELETE from Client_phone WHERE client_id=%s;
                    """
            cursor.execute(query, (client_id, ))
            if cursor.rowcount == 0:
                cursor.connection.rollback()
                print(f'У клиента {client_id} нет номеров телефона')
            else:
                cursor.connection.commit()
                print(f'Номера телефонов удалены для клиента {client_id}')
    else:
        if phone_number:
            query = f"""
            DELETE from Client_phone WHERE client_id=%s and phone_number=%s;
            """
            cursor.execute(query, (client_id, phone_number))
            if cursor.rowcount == 0:
                cursor.connection.rollback()
                print(f'Номер телефона {phone_number} не найден для клиента {client_id}')
            else:
                cursor.connection.commit()
                print(f'Номер телефона {phone_number} удален для клиента {client_id}')
        else:
            query = f"""
                    DELETE from Client_phone WHERE client_id=%s;
                    """
            cursor.execute(query, (client_id, ))
            if cursor.rowcount == 0:
                cursor.connection.rollback()
                print(f'У клиента {client_id} нет номеров телефона')
            else:
                cursor.connection.commit()
                print(f'Номера телефонов удалены для клиента {client_id}')

def delete_client(cursor, id, email):
    """
    Удаляет клиента из базы данных.

    Аргументы:
    - cursor: объект курсора для выполнения SQL-запросов.
    - id: ID клиента (если известен).
    - email: email клиента (если ID не указан).

    Исключения:
    - Если клиент не найден, удаление откатывается.
    """

    if id is None:
        id = get_client_id(cursor, email)
        if id:
            query = """
            DELETE from Client WHERE id=%s;
            """
            cursor.execute(query, (id, ))
            cursor.connection.commit()
            print(f'Клиент {id} c email {email} удален')
    else:
        query = """
                DELETE from Client WHERE id=%s;
                """
        cursor.execute(query, (id,))
        if cursor.rowcount == 0:
            cursor.connection.rollback()
            print(f'В БД отсутствует клиент с id {id}')
        else:
            cursor.connection.commit()
            print(f'Клиент с id {id} удален из БД')

def find_client(cursor, first_name=None, last_name=None, email=None, phone_number=None):
    """
    Ищет клиента по имени, фамилии, email или номеру телефона.

    Аргументы:
    - cursor: объект курсора для выполнения SQL-запросов.
    - first_name: имя клиента (опционально).
    - last_name: фамилия клиента (опционально).
    - email: email клиента (опционально).
    - phone_number: номер телефона клиента (опционально).

    Возвращает:
    - Список клиентов, соответствующих критериям поиска, или сообщение о том, что клиент не найден.
    """
    if phone_number != '' and phone_number is not None:
        query = """
        SELECT c.id, c.first_name, c.last_name, c.email from Client as c
        JOIN Client_phone as cp on c.id = cp.client_id
        WHERE cp.phone_number = %s;
        """
        cursor.execute(query, (phone_number, ))
        if cursor.rowcount == 0:
            cursor.connection.rollback()
            print(f'В БД отсутствует клиент с телефоном {phone_number}')
        else:
            result = cursor.fetchall()
            print(result)
            if first_name is not None or last_name is not None or email is not None:
                for client in result:
                    if client[1] != first_name or client[2] != last_name or client[3] != email:
                        print('Проверьте правильность указания имени и/или фамилии и/или email при вызове функции')
    else:
        if email != '' and email is not None:
            query = """
            SELECT * FROM Client WHERE email = %s;
            """
            cursor.execute(query, (email, ))
            if cursor.rowcount == 0:
                cursor.connection.rollback()
                print(f'В БД отсутствует клиент с email {email}')
            else:
                result = cursor.fetchall()
                print(result)
                if first_name is not None or last_name is not None or email is not None:
                    for client in result:
                        if client[1] != first_name or client[2] != last_name or client[3] != email:
                            print('Проверьте правильность указания имени и/или фамилии и/или email при вызове функции')
        else:
            query = """
            SELECT * FROM Client WHERE first_name = %s and last_name = %s;
            """
            cursor.execute(query, (first_name, last_name))
            if cursor.rowcount == 0:
                cursor.connection.rollback()
                print(f'В БД отсутствует клиент с сочетанием имени {first_name} и фамилии {last_name}')
            else:
                print(cursor.fetchall())
