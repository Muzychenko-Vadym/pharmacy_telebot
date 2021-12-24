# -*- coding: utf-8 -*-
"""
Цей файл містить функції, необхідні для
хешування паролів
"""

import uuid
import hashlib


def hash_password(password):
    """
    Ця функція виконує хешування паролю
        :param password: пароль
        :return result: хешований пароль.
    """
    # uuid використовується для генерації випадкового числа
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    """
    Ця функція виконує перевірку паролю відповідно до захешованого варіанту
        :param hashed_password: хешований пароль
        :param user_password: звичайний пароль
        :return result: результат порівняння (True or False) .
    """
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
