# -*- coding: utf-8 -*-
"""
Цей файл містить функції, необхідні для
реєстрації користувача
"""

import random
import re

from telebot import types

import mail
import database
import hash_password
import user_workspace

from keyboards import keyboard_yes_no

from help_functions import input_check


def is_age(i):
    try:
        i = int(i)
        if((i > 6) and (i < 120)):
            return True
        return False
    except:
        return False


def registration(message, bot):
    """ Функція прийому пошти """
    user_email = message.text.lower()
    if (re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)", message.text.lower())):
        msg = bot.send_message(message.chat.id,
                               "Ваша пошта "+user_email+" ?",
                               reply_markup=keyboard_yes_no())
        bot.register_next_step_handler(msg, reg_step_1, bot, user_email)
    else:
        msg2 = bot.send_message(message.chat.id,
                                "Веедене вами повідомлення не є поштовою адресою. Надішліть, будь ласка, свою пошту.\nПриклад:\nexample@mail.com")
        bot.register_next_step_handler(msg2, registration, bot)


def reg_step_1(message, bot, user_email):
    """ Функція покрокової реєстрації """
    if(message.text == "Так"):
        rnd_code = random.randint(100, 1000)

        # надсилання коду на пошту
        mail.send_to_email(user_email, rnd_code)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=(True),
                                             one_time_keyboard=(True))
        button = types.KeyboardButton("Ввести пошту заново")
        keyboard.add(button)

        msg = bot.send_message(message.chat.id,
                               "На вашу пошту було надіслано код підтвердження. Введіть код підтвердження:",
                               reply_markup=keyboard)
        bot.register_next_step_handler(
            msg, reg_step_2, bot, rnd_code, user_email)
    else:
        msg2 = bot.send_message(message.chat.id, "Надішліть свою пошту")
        bot.register_next_step_handler(msg2, registration, bot)


def reg_step_2(message, bot, rnd_code, user_email):
    """ Функція покрокової реєстрації """
    if(message.text == str(rnd_code)):
        msg = bot.send_message(
            message.chat.id, "Введіть своє прізвище та ім'я (через пробіл)")
        bot.register_next_step_handler(msg, reg_step_3, bot, user_email)
    elif(message.text == "Ввести пошту заново"):
        # bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(message.chat.id, "Надішліть свою пошту")
        bot.register_next_step_handler(msg, registration, bot)
    else:
        msg2 = bot.send_message(
            message.chat.id, "Коди не співпадають, надішліть свою пошту")
        bot.register_next_step_handler(msg2, registration, bot)


def reg_step_3(message, bot, user_email):
    """ Функція покрокової реєстрації """
    user_name = message.text
    # перевірка на наявність заборонених символів
    if input_check(user_name):
        msg = bot.send_message(message.chat.id, "Введіть свій вік")
        bot.register_next_step_handler(
            msg, reg_step_4, bot, user_email, user_name)
    else:
        msg = bot.send_message(
            message.chat.id, "Ваше ім'я не повинно містити заборонених символів! ( ' \";:*)\nВведіть своє ім'я")
        bot.register_next_step_handler(msg, reg_step_3, bot, user_email)


def reg_step_4(message, bot, user_email, user_name):
    """ Функція покрокової реєстрації """
    user_age = message.text
    if (is_age(user_age)):
        msg = bot.send_message(message.chat.id, "Придумайте пароль")
        bot.register_next_step_handler(
            msg, reg_step_5, bot, user_email, user_name, user_age)
    else:
        msg = bot.send_message(message.chat.id,
                               "Вік введено не вірно. Введіть свій вік")
        bot.register_next_step_handler(
            msg, reg_step_4, bot, user_email, user_name)


def reg_step_5(message, bot, user_email, user_name, user_age):
    """ Функція покрокової реєстрації """
    user_password = message.text
    msg = bot.send_message(message.chat.id, "Введіть пароль ще раз")
    bot.register_next_step_handler(
        msg, reg_step_6, bot, user_email, user_name, user_age, user_password)


def reg_step_6(message, bot, user_email, user_name, user_age, user_password):
    """ Функція покрокової реєстрації """
    if (user_password == message.text):
        msg = bot.send_message(message.chat.id,
                               "Перегляньте чи співпадають дані:\nВаша пошта: "+user_email +
                               ",\nВаше ім'я та прізвище: "+user_name +
                               ",\nВаш вік: "+user_age+" ?",
                               reply_markup=keyboard_yes_no())
        bot.register_next_step_handler(
            msg, reg_step_7, bot, user_email, user_name, user_age, user_password)
    else:
        bot.send_message(message.chat.id, "Паролі не співпадають!")
        msg = bot.send_message(message.chat.id, "Введіть пароль")
        bot.register_next_step_handler(
            msg, reg_step_5, bot, user_email, user_name, user_age)


def reg_step_7(message, bot, user_email, user_name, user_age, user_password):
    """ Функція покрокової реєстрації """
    if(message.text == "Так"):
        user_hashed_pass = hash_password.hash_password(user_password)
        database.user_registration(message.from_user.id,
                                   user_email,
                                   user_name,
                                   user_hashed_pass,
                                   user_age)
        bot.send_message(message.chat.id,
                         "Вас зареєстровано. Ваш телеграм профіль прив'язаний до бази даних, тому немає необхідності щоразу при старті /start вводити пошту та пароль.")
        user_workspace.start_workspace(message, bot)
    else:
        msg = bot.send_message(message.chat.id,
                               "Введіть своє прізвище та ім'я, які розділені пробілом")
        bot.register_next_step_handler(msg, reg_step_3, bot, user_email)
