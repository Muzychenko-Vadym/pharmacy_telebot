# -*- coding: utf-8 -*-
"""
Цей файл містить функції, необхідні для
роботи користувача "user"
"""
from telebot import types

import database

from keyboards import keyboard_main_menu
from keyboards import back_to_main_menu
from keyboards import list_keyboard
from keyboards import clear_keyboard
from keyboards import user_list_order_keyboard

from help_functions import to_list
from help_functions import date_to_string


def start_workspace(message, bot):
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.send_message(message.chat.id, "Головне меню",
                     reply_markup=keyboard_main_menu())


def medicine_list(message, bot):
    """ Функція виведення списку ліків """
    try:
        bot.send_message(
            message.chat.id,
            "Список",
            reply_markup=list_keyboard(
                to_list(database.select_operation(
                    "SELECT name FROM medicine;"))
            ),
        )
    except:
        bot.send_message(
            message.chat.id,
            "Список ліків пустий! Мабуть, сталася якась помилка!",
            reply_markup=back_to_main_menu(),
        )


def choose_medicine(message, bot, name):
    """ Функція виведення інформації про медикамент """
    text = database.select_operation(
        "SELECT text FROM medicine WHERE name = '" + str(name) + "';")
    age = database.select_operation(
        "SELECT age FROM medicine WHERE name = '" + str(name) + "';")
    price = database.select_operation(
        "SELECT price FROM medicine WHERE name = '" + str(name) + "';")
    prescription_bool = database.select_operation(
        "SELECT prescription FROM medicine WHERE name = '" + str(name) + "';")
    med_id = database.select_operation(
        "SELECT id FROM medicine WHERE name = '" + str(name) + "';")
    if prescription_bool == "1":
        prescription = "Потрібен"
    else:
        prescription = "Непотрібен"
    s = "user_show_medicine|" + med_id
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Купити", callback_data=s)
    button2 = types.InlineKeyboardButton(
        text="Назад", callback_data="user_medicine_list"
    )
    keyboard.add(button1, button2)
    bot.send_message(
        message.chat.id,
        name
        + "\nОпис: "
        + text
        + "\nМінімальний вік прийому препарату: "
        + age
        + "\nРецепт від лікаря: "
        + prescription
        + "\nЦіна: "
        + price,
        reply_markup=keyboard,
    )


def order_medicine(message, bot, medicine_id):
    """ Функція придбання медикаменту """
    prescription = database.select_operation(
        "SELECT prescription FROM medicine WHERE id = " +
        str(medicine_id) + ";"
    )
    if prescription == "1":
        prescription_id = database.select_operation(
            "SELECT id FROM `prescription` WHERE id_medicine ="
            + str(medicine_id)
            + " AND id_client = "
            + str(message.chat.id)
            + ";"
        )
        if prescription_id != "":
            order_medicine_step_1(message, bot, medicine_id)
        else:
            bot.send_message(
                message.chat.id,
                "У Вас відсутній рецепт на цей препарат. Даний препарат видається тільки по рецепту від лікаря.",
                reply_markup=back_to_main_menu(),
            )
    else:
        order_medicine_step_1(message, bot, medicine_id)


def order_medicine_step_1(message, bot, med_id):
    """ Функція покрокової покупки медикаменту """
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=(True), row_width=2, one_time_keyboard=(True)
    )
    button1 = types.KeyboardButton("Так")
    button2 = types.KeyboardButton("Ні")
    keyboard.add(button1, button2)
    msg = bot.send_message(
        message.chat.id, "У Вас є наша бонусна картка?", reply_markup=keyboard
    )
    bot.register_next_step_handler(msg, order_medicine_step_2, bot, med_id)


def order_medicine_step_2(message, bot, med_id):
    """ Функція покрокової покупки медикаменту """
    if message.text == "Так":
        bonuscard = True
    elif message.text == "Ні":
        bonuscard = False
    else:
        msg2 = bot.send_message(
            message.chat.id, "У Вас є наша бонусна картка?")
        bot.register_next_step_handler(
            msg2, order_medicine_step_2, bot, med_id)
        return
    # перевірка дозволеного віку прийому препарату
    # наступний блок
    try:
        if int(database.select_operation(
                "SELECT age FROM client WHERE id =" +
            str(message.chat.id) + ";"
            )
        ) < int(database.select_operation(
                "SELECT age FROM medicine WHERE id =" + str(med_id) + ";"
            )
        ):
            bot.send_message(
                message.chat.id,
                "Вибачте, але ваш вік є меншим за дозволений вік прийому препарату.",
                reply_markup=back_to_main_menu(),
            )
    except:
        # якщо message.chat.id не співпадає із id_client
        bot.send_message(
            message.chat.id,
            "Немає дозволу на виконання даної операції! Можливо Ви ввійшли з іншого профілю"
        )
    else:
        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=(True), row_width=2, one_time_keyboard=(True)
        )
        button1 = types.KeyboardButton("Я біля магазину, хочу стати в чергу")
        button2 = types.KeyboardButton("Замовити доставку")
        keyboard.add(button1, button2, row_width=1)
        msg = bot.send_message(
            message.chat.id, "Як бажаєте отримати ліки?", reply_markup=keyboard
        )
        bot.register_next_step_handler(
            msg, order_medicine_step_3, bot, med_id, bonuscard
        )


def order_medicine_step_3(message, bot, med_id, bonuscard):
    """ Функція покрокової покупки медикаменту """
    if message.text == "Я біля магазину, хочу стати в чергу":
        order_id = database.order_registration(
            message.chat.id, "1", med_id, bonuscard)
        if order_id == None:
            bot.send_message(
                message.chat.id,
                "Немає дозволу на виконання даної операції! Можливо Ви ввійшли з іншого профілю"
            )
        else:
            bot.send_message(
                message.chat.id,
                "Чудово, очікуйте в черзі, Ваше замовлення - № " +
                str(order_id),
                reply_markup=clear_keyboard(),
            )  # back_to_main_menu())
            start_workspace(message, bot)
    elif message.text == "Замовити доставку":
        bot.send_message(
            message.chat.id,
            "Нажаль, зараз ця функція недоступна",
            reply_markup=back_to_main_menu(),
        )
    else:
        msg = bot.send_message(
            message.chat.id,
            "Як бажаєте отримати ліки? Введіть або виберіть\n'Я біля магазину, хочу стати в чергу' або 'Замовити доставку'",
        )
        bot.register_next_step_handler(
            msg, order_medicine_step_3, bot, med_id, bonuscard
        )


def order_list(message, bot):
    """ Функція виведення списку замовлень """
    try:
        bot.send_message(
            message.chat.id,
            "Список ваших замовлень",
            reply_markup=user_list_order_keyboard(
                to_list(
                    database.select_operation(
                        "SELECT id FROM `order` WHERE id_client="
                        + str(message.chat.id)
                        + ";"
                    )
                )
            ),
        )
    except:
        bot.send_message(
            message.chat.id,
            "Список замовлень пустий! Ви ще не зробили жодного замовлення",
            reply_markup=back_to_main_menu(),
        )


def choose_order(message, bot, order_id):
    """ Функція виведення інформації про замовлення """
    medicine_id = database.select_operation(
        "SELECT id_medicine FROM `order` WHERE id = " + str(order_id) + ";")
    name = database.select_operation(
        "SELECT name FROM medicine WHERE id = '" + str(medicine_id) + "';")
    age = database.select_operation(
        "SELECT age FROM medicine WHERE id = '" + str(medicine_id) + "';")
    price = database.select_operation(
        "SELECT price FROM medicine WHERE id = '" + str(medicine_id) + "';")
    prescription_bool = database.select_operation(
        "SELECT prescription FROM medicine WHERE id = '" +
        str(medicine_id) + "';")
    provizor_id = database.select_operation(
        "SELECT id_provizor FROM `order` WHERE id = " + str(order_id) + ";")
    order_time = database.select_operation(
        "SELECT datatime FROM `order` WHERE id = " + str(order_id) + ";")
    status_bool = database.select_operation(
        "SELECT status FROM `order` WHERE id = " + str(order_id) + ";")

    if prescription_bool == "1":
        prescription = "Потрібен"
    else:
        prescription = "Непотрібен"
    if status_bool == "1":
        status = "Виконано"
    else:
        status = "В обробці"
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text="Назад", callback_data="user_order")
    keyboard.add(button, row_width=1)
    bot.send_message(
        message.chat.id,
        "Id замовлення: "
        + order_id
        + "\nНазва: "
        + name
        + "\nРецепт від лікаря: "
        + prescription
        + "\nId обслуговуючого персоналу, який виконав замовлення: "
        + provizor_id
        + "\nЧас створення замовлення:\n"
        + date_to_string(order_time)
        + "\nЦіна: "
        + price
        + "\n Статус виконнання: "
        + status,
        reply_markup=keyboard,
    )


def personal_account(message, bot):
    """ Функція виведення інформації про користувача """
    name = database.select_operation(
        "SELECT name FROM `client` WHERE id = " + str(message.chat.id) + ";"
    )
    age = database.select_operation(
        "SELECT age FROM `client` WHERE id = " + str(message.chat.id) + ";"
    )
    bot.send_message(
        message.chat.id,
        "Ваш профіль\nId користувача:\n  "
        + str(message.chat.id)
        + "\nІм'я:\n  "
        + name
        + "\nВік: "
        + age,
        reply_markup=back_to_main_menu(),
    )


def about(message, bot):
    """ Функція виведення інформації про бота """
    bot.send_message(
        message.chat.id,
        "@pharmacyTestBot створено як альтернативу веб-формі для захисту лабораторної роботи із предмету Організація баз даних.\nБот демонструє роботу функцій взаємодії Python та бази даних.\nРозробниками бота є студенти групи КІ-202 Музиченко Вадим та Овсяник Владислав.",
        reply_markup=back_to_main_menu(),
    )
