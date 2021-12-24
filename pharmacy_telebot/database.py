# -*- coding: utf-8 -*-
"""
Цей файл містить функції, які використовуються
для роботи із базою даних
"""

import time

from mysql.connector import connect, Error

from help_functions import to_string


def operation_users(operation):
    """
    Ця функція виконує запит у окремій базі
    даних користувачів та повертає значення
        :param operation: запит мовою SQL
        :return result: результат виконання запиту.
    """
    try:
        with connect(
            host="localhost", user="root", password="", database="pharmacy_users"
        ) as connection:
            select_movies_query = operation
            with connection.cursor() as cursor:
                cursor.execute(select_movies_query)
                result = cursor.fetchall()
                return to_string(result)
    except Error as e:
        print(e)


def select_operation(operation):
    """
    Ця функція виконує запит у базі даних та повертає значення
        :param operation: запит мовою SQL
        :return result: - результат виконання запиту.
    """
    try:
        with connect(
            host="localhost", user="root", password="", database="pharmacy_1"
        ) as connection:
            select_movies_query = operation
            with connection.cursor() as cursor:
                cursor.execute(select_movies_query)
                result = cursor.fetchall()
                return to_string(result)
    except Error as e:
        print(e)
        return None


def user_registration(user_id, email, name, password, age):
    """
    Ця функція виконує реєстрацію користувача у базі даних
        :param user_id: id користувача (первинний ключ)
        :param email: пошта користувача
        :param name: ім'я користувача'
        :param password: пароль
        :param age: вік користувача
    """
    try:
        with connect(
            host="localhost", user="root", password="", database="pharmacy_users"
        ) as connection:
            insert_movies_query = (
                "INSERT INTO users VALUES ("
                + str(user_id)
                + ", '"
                + password
                + "', false, false, false);"
            )
            with connection.cursor() as cursor:
                cursor.execute(insert_movies_query)
                connection.commit()

                with connect(
                    host="localhost", user="root", password="", database="pharmacy_1"
                ) as connection:
                    insert_movies_query2 = (
                        "INSERT INTO `client` VALUES ("
                        + str(user_id)
                        + ", '"
                        + name
                        + "', '"
                        + email
                        + "', "
                        + str(age)
                        + ");"
                    )
                    with connection.cursor() as cursor:
                        cursor.execute(insert_movies_query2)
                        connection.commit()
    except Error as e:
        print(e)


def user_autorization(email):
    """
    Ця функція виконує авторизацію користувача
        :param email: пошта користувача
        :return user_password: хешований пароль користувача.
    """
    try:
        with connect(
            host="localhost", user="root", password="", database="pharmacy_1"
        ) as connection:
            select_id = (
                "SELECT id FROM pharmacy_1.client WHERE email = '" + email + "';"
            )
            with connection.cursor() as cursor:
                cursor.execute(select_id)
                user_id = str(cursor.fetchall()).replace(
                    "[(", "").replace(",)]", "")
                with connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="pharmacy_users",
                ) as connection:
                    select_password = (
                        "SELECT password FROM pharmacy_users.users  WHERE id = "
                        + str(user_id)
                        + ";"
                    )
                    with connection.cursor() as cursor2:
                        cursor2.execute(select_password)
                        user_password = cursor2.fetchall()
                        return to_string(user_password)
    except Error as e:
        print(e)
        return None


def user_verification(user_id):
    """
    Ця функція виконує верифікацію користувача
        :param user_id: id користувача
        :return: повертає True або False в залежності
                 від того, чи є такий користувач в базі.
    """
    try:
        with connect(
            host="localhost", user="root", password="", database="pharmacy_users"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                      id
                    FROM
                      users
                    WHERE
                      id = %(id)s
                    """,
                    {"id": user_id},
                )
                user_id_db = str(cursor.fetchall()).replace(
                    "[(", "").replace(",)]", "")
                if user_id_db == str(user_id):
                    return True
                else:
                    return False
    except Error as e:
        print(e)
        return False


def order_registration(user_id, provizor_id, med_id, bonuscard):
    """
    Ця функція виконує реєстрацію замовлення
        :param user_id: id користувача
        :param provizor_id: id провізора
        :param med_id: id препарату
        :param bonuscard: наявність бонусної карти
        :return cursor.lastrowid(): повертає id створеного замовлення.
    """
    try:
        with connect(
            host="localhost", user="root", password="", database="pharmacy_1"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO 
                      `order`
                    VALUES (
                      0,
                      %(bonuscard)s,
                      %(user_id)s,
                      NULL,
                      0,
                      %(time)s,
                      %(med_id)s,
                      NULL );
                    """,
                    {
                        "bonuscard": bonuscard,
                        "user_id": user_id,
                        "provizor_id": provizor_id,
                        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "med_id": med_id,
                    },
                )
                connection.commit()
                return cursor.lastrowid
    except Error as e:
        print(e)
        return None


def order_done(order_id, provizor_id):
    """
    Ця функція виконує змінює статус замовлення у базі даних
        :param order_id: id замовлення
    """
    try:
        with connect(
            host="localhost", user="root", password="", database="pharmacy_1"
        ) as connection:
            with connection.cursor() as cursor:
                order_table = (
                    "UPDATE `order` SET status=1, id_provizor="
                    + str(provizor_id)
                    + " WHERE id = "
                    + str(order_id)
                    + ";"
                )
                cursor.execute(order_table)
                connection.commit()
    except Error as e:
        print(e)
        return None


def prescription_registration(medicine_id, client_id, doctor_id):
    """
    Ця функція виконує реєстрацію рецепта
        :param medicine_id: id препарату
        :param client_id: id користувача
        :param doctor_id: id лікаря
    """
    try:
        with connect(
            host="localhost", user="root", password="", database="pharmacy_1"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO
                      `prescription`
                    VALUES (
                      0,
                      %(doctor_id)s,
                      %(client_id)s,
                      %(medicine_id)s,
                      %(time)s );
                    """,
                    {
                        "doctor_id": doctor_id,
                        "client_id": client_id,
                        "medicine_id": medicine_id,
                        "time": str(time.strftime("%Y-%m-%d %H:%M:%S")),
                    },
                )
                connection.commit()
    except Error as e:
        print(e)


def delete_operation(operation):
    """
    Ця функція виконує запит видалення у базі даних
        :param operation: запит мовою SQL
    """
    try:
        with connect(
            host="localhost", user="root", password="", database="pharmacy_1"
        ) as connection:
            delete_query = operation
            with connection.cursor() as cursor:
                cursor.execute(delete_query)
                connection.commit()
    except Error as e:
        print(e)


def user_autorization_id_update(user_email, user_id, old_id):
    """
    Ця функція виконує змінює статус замовлення у базі даних
        :param order_id: id замовлення
    """
    try:
        with connect(
            host="localhost", user="root", password="", database="pharmacy_1"
        ) as connection:
            with connection.cursor() as cursor:
                order_table = (
                    "UPDATE `client` SET id="
                    + str(user_id)
                    + " WHERE email = '"
                    + str(user_email)
                    + "';"
                )
                cursor.execute(order_table)
                connection.commit()

                with connect(
                    host="localhost",
                    user="root", password="",
                    database="pharmacy_users"
                ) as connection:
                    with connection.cursor() as cursor:
                        order_table = (
                            "UPDATE `users` SET id="
                            + str(user_id)
                            + " WHERE id = "
                            + str(old_id)
                            + ";"
                        )
                        cursor.execute(order_table)
                        connection.commit()

    except Error as e:
        print(e)
        return None
