# -*- coding: utf-8 -*-
"""
Цей файл містить допоміжні функції
"""

import re


def to_string(lis):
    return str(lis).replace("(", "").replace(")", "").replace(",", "").replace("[", "").replace("'", "").replace("]", "")


def edit_list(l):
    string = str(l).replace("(", "").replace(")", "").replace(
        ",", "").replace("[", "").replace("'", "").replace("]", "")
    return list(string.split(" "))


def to_list(string):
    return list(string.split(" "))


def date_to_string(string):
    return string.replace("datetime.datetime", "", 1).replace(" ", "/", 2).replace(" ", ":", 3).replace(":", ", ", 1)


def input_check(string):
    """
    Ця функція перевірку на наявність заборонених символів
        :param string: рядок, який потрібно обробити
        :return: результат виконання обробки (True or False).
    """
    if re.search(r"['\";:\*]+", string):
        return False  # якщо рядок містить заборонені символи
    else:
        return True
