# -*- coding: utf-8 -*-
"""
Цей файл містить функції, необхідні для
роботи користувача "provizor"
"""

from telebot import types

import database

from keyboards import keyboard_provizor_main_menu
from keyboards import list_order_keyboard
from keyboards import back_to_main_menu_provizor
from keyboards import back_to_order_list
from keyboards import list_order_done_keyboard

from help_functions import to_list
from help_functions import date_to_string


def start_workspace(message, bot):
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.send_message(message.chat.id, "Головне меню",
                     reply_markup=keyboard_provizor_main_menu())


def order_list(message, bot):
    """ Функція виведення списку замовлень """
    try:
        bot.send_message(message.chat.id, "Список замовлень",
                         reply_markup=list_order_keyboard(to_list(database.select_operation("SELECT id FROM `order` WHERE status=0;"))))
    except:
        bot.send_message(message.chat.id, "Список замовлень пустий! Спробуйте трішки пізніше, поки з'являться нові замовлення!",
                         reply_markup=back_to_main_menu_provizor())


def order_done_list(message, bot):
    """ Функція виведення списку виконаних замовлень """
    try:
        bot.send_message(message.chat.id, "Список виконаних замовлень",
                         reply_markup=list_order_done_keyboard(to_list(database.select_operation("SELECT id FROM `order` WHERE status=1;"))))
    except:
        bot.send_message(message.chat.id, "Список замовлень пустий! Спробуйте трішки пізніше, поки з'являться нові замовлення!",
                         reply_markup=back_to_main_menu_provizor())


def choose_order(message, bot, order_id):
    """ Функція виведення інформації про замовлення """
    medicine_id = database.select_operation(
        "SELECT id_medicine FROM `order` WHERE id = "+str(order_id)+";")
    name = database.select_operation(
        "SELECT name FROM medicine WHERE id = '"+str(medicine_id)+"';")
    age = database.select_operation(
        "SELECT age FROM medicine WHERE id = '"+str(medicine_id)+"';")
    price = database.select_operation(
        "SELECT price FROM medicine WHERE id = '"+str(medicine_id)+"';")
    prescription_bool = database.select_operation(
        "SELECT prescription FROM medicine WHERE id = '"+str(medicine_id)+"';")

    client_id = database.select_operation(
        "SELECT id_client FROM `order` WHERE id = "+str(order_id)+";")

    client_name = database.select_operation(
        "SELECT name FROM `client` WHERE id = "+str(client_id)+";")
    order_time = database.select_operation(
        "SELECT datatime FROM `order` WHERE id = "+str(order_id)+";")
    if(prescription_bool == "1"):
        prescription = "Потрібен"
    else:
        prescription = "Непотрібен"
    s = "provizor_order_done|" + order_id
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text="Замовлення виконано", callback_data=s)
    button2 = types.InlineKeyboardButton(
        text="Назад", callback_data="provizor_order_list")
    keyboard.add(button1, button2, row_width=1)
    bot.send_message(message.chat.id,
                     "Id замовлення: "+order_id +
                     "\nНазва: "+name +
                     "\nЗамовник: "+client_name +
                     "\nРецепт від лікаря: "+prescription +
                     "\nЧас створення замовлення:\n"+date_to_string(order_time) +
                     "\nЦіна: "+price,
                     reply_markup=keyboard)


def order_medicine(message, bot, order_id):
    """ Функція виведення зміни статусу виконання замовлення """
    database.order_done(order_id, message.chat.id)
    bot.send_message(message.chat.id, "Замовлення виконано!",
                     reply_markup=back_to_order_list())


def choose_order_done(message, bot, order_id):
    """ Функція виведення інформації про виконане замовлення """
    medicine_id = database.select_operation(
        "SELECT id_medicine FROM `order` WHERE id = "+str(order_id)+";")
    name = database.select_operation(
        "SELECT name FROM medicine WHERE id = '"+str(medicine_id)+"';")
    price = database.select_operation(
        "SELECT price FROM medicine WHERE id = '"+str(medicine_id)+"';")
    prescription_bool = database.select_operation(
        "SELECT prescription FROM medicine WHERE id = '"+str(medicine_id)+"';")
    client_id = database.select_operation(
        "SELECT id_client FROM `order` WHERE id = "+str(order_id)+";")
    client_name = database.select_operation(
        "SELECT name FROM `client` WHERE id = "+str(client_id)+";")
    order_time = database.select_operation(
        "SELECT datatime FROM `order` WHERE id = "+str(order_id)+";")
    if(prescription_bool == "1"):
        prescription = "Наявний"
    else:
        prescription = "Непотрібен"
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text="Назад", callback_data="provizor_order_done_list")
    keyboard.add(button, row_width=1)
    bot.send_message(
        message.chat.id,
        "Id замовлення: "+order_id +
        "\nНазва: "+name +
        "\nЗамовник: "+client_name +
        "\nРецепт від лікаря: "+prescription +
        "\nЧас створення замовлення:\n"+date_to_string(order_time) +
        "\nЦіна: "+price,
        reply_markup=keyboard)


def personal_account(message, bot):
    """ Функція виведення інформації про провізора """
    name = database.select_operation(
        "SELECT name FROM `provizor` WHERE id = "+str(message.chat.id)+";")
    bot.send_message(
        message.chat.id,
        "Ваш профіль\nId провізора:\n  " +
        str(message.chat.id)+"\nІм'я:\n  "+name,
        reply_markup=back_to_main_menu_provizor())


def about(message, bot):
    """ Функція виведення інформації про бота """
    bot.send_message(
        message.chat.id,
        "@pharmacyTestBot створено як альтернативу веб-формі для захисту лабораторної роботи із предмету Організація баз даних.\nБот демонструє роботу функцій взаємодії Python та бази даних.\nРозробниками бота є студенти групи КІ-202 Музиченко Вадим та Овсяник Владислав.",
        reply_markup=back_to_main_menu_provizor())
