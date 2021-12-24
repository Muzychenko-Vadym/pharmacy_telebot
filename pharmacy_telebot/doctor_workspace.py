# -*- coding: utf-8 -*-
"""
Цей файл містить функції, необхідні для
роботи користувача "doctor"
"""

from telebot import types

import database

from keyboards import keyboard_doctor_main_menu
from keyboards import list_med_doctor_keyboard
from keyboards import back_to_main_menu_doctor
from keyboards import keyboard_yes_no
from keyboards import keyboard_back

from help_functions import to_list


def is_int(i):
    try:
        i = int(i)
        return True
    except:
        return False


def start_workspace(message, bot):
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.send_message(message.chat.id, "Головне меню",
                     reply_markup=keyboard_doctor_main_menu())


def write_prescription(message, bot):
    """ Функція виведення списку ліків, для покупки яких потрібен рецепт """
    try:
        bot.send_message(
            message.chat.id,
            "Виберіть препарат, для якого потрібно виписати рецепт.\nСписок ліків, для купівлі яких потрібен рецепт:",
            reply_markup=list_med_doctor_keyboard(to_list(database.select_operation(
                "SELECT name FROM `medicine` WHERE prescription=1;")))
        )
    except:
        bot.send_message(message.chat.id, "Список ліків, для купівлі яких потрібен рецепт, пустий! Спробуйте трішки пізніше, можливо виникла якась помилка!",
                         reply_markup=back_to_main_menu_doctor())


def choose_medicine(message, bot, name):
    """ Функція виведення інформації про медикамент """
    text = database.select_operation(
        "SELECT text FROM medicine WHERE name = '"+str(name)+"';")
    age = database.select_operation(
        "SELECT age FROM medicine WHERE name = '"+str(name)+"';")
    price = database.select_operation(
        "SELECT price FROM medicine WHERE name = '"+str(name)+"';")
    med_id = database.select_operation(
        "SELECT id FROM medicine WHERE name = '"+str(name)+"';")
    s = "doctor_enter_medicine|" + med_id
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Вибрати", callback_data=s)
    button2 = types.InlineKeyboardButton(
        text="Назад", callback_data="doctor_write_prescription")
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, name +
                     "\nОпис: "+text +
                     "\nМінімальний вік прийому препарату: "+age +
                     "\nЦіна: "+price,
                     reply_markup=keyboard)


def write_prs_step_2(message, bot, medicine_id):
    """ Функція покрокового виписування рецепту """
    msg = bot.send_message(
        message.chat.id, "Введіть id пацієнта, якому потрібно виписати ліки", reply_markup=keyboard_back())
    bot.register_next_step_handler(msg, write_prs_step_3, bot, medicine_id)


def write_prs_step_3(message, bot, medicine_id):
    """ Функція покрокового виписування рецепту """
    client_id = message.text
    if (is_int(client_id) == True):
        name = database.select_operation(
            "SELECT name  FROM `client` WHERE id = "+client_id+";")
        age = database.select_operation(
            "SELECT age  FROM `client` WHERE id = "+client_id+";")

        if(name != ""):
            msg = bot.send_message(message.chat.id, "Дані вибраного пацієнта:\nПрізвище та ім'я:"+str(
                name)+"\nВік: "+str(age)+"\nУсе вірно?", reply_markup=keyboard_yes_no())
            bot.register_next_step_handler(
                msg, write_prs_step_4, bot, medicine_id, client_id)
        else:
            bot.send_message(message.chat.id, "Такого пацієнта не знайдено")
            write_prs_step_2(message, bot, medicine_id)

    elif(client_id == "Повернутись до головного меню"):
        start_workspace(message, bot)
    else:
        bot.send_message(message.chat.id, "Id має містити тільки числа")
        write_prs_step_2(message, bot, medicine_id)


def write_prs_step_4(message, bot, medicine_id, client_id):
    """ Функція покрокового виписування рецепту """
    if(message.text == "Так"):
        database.prescription_registration(
            medicine_id, client_id, message.chat.id)
        bot.send_message(message.chat.id, "Чудово, рецепт виписано",
                         reply_markup=back_to_main_menu_doctor())
    elif(message.text == "Ні"):
        bot.send_message(message.chat.id, "Введіть усі дані заново")
        write_prescription(message, bot)


def personal_account(message, bot):
    """ Функція виведення інформації про лікаря """
    name = database.select_operation(
        "SELECT name FROM `doctor` WHERE id = "+str(message.chat.id)+";")
    typ = database.select_operation(
        "SELECT type FROM `doctor` WHERE id = "+str(message.chat.id)+";")
    bot.send_message(
        message.chat.id,
        "Ваш профіль\nId лікаря:\n  " +
        str(message.chat.id)+"\nІм'я:\n  "+name+"\nСпеціалізація:\n  "+typ,
        reply_markup=back_to_main_menu_doctor())


def about(message, bot):
    """ Функція виведення інформації про бота """
    bot.send_message(
        message.chat.id,
        "@pharmacyTestBot створено як альтернативу веб-формі для захисту лабораторної роботи із предмету Організація баз даних.\nБот демонструє роботу функцій взаємодії Python та бази даних.\nРозробниками бота є студенти групи КІ-202 Музиченко Вадим та Овсяник Владислав.",
        reply_markup=back_to_main_menu_doctor())
