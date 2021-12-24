# -*- coding: utf-8 -*-
"""
Цей файл містить функції, які використовуються
для створення об'єктів InlineKeyboardMarkup 
та ReplyKeyboardMarkup 
"""

from telebot import types


def keyboard_main_menu():
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text="Переглянути список ліків", callback_data="user_medicine_list")
    button2 = types.InlineKeyboardButton(
        text="Переглянути список замовлень", callback_data="user_order")
    button3 = types.InlineKeyboardButton(
        text="Особистий кабінет", callback_data="user_personal_account")
    button4 = types.InlineKeyboardButton(
        text="Інформація про бота", callback_data="user_about")
    keyboard.add(button1, button2, button3, button4, row_width=1)
    return keyboard


def keyboard_provizor_main_menu():
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text="Переглянути список замовлень", callback_data="provizor_order_list")
    button2 = types.InlineKeyboardButton(
        text="Переглянути список виконаних замовлень", callback_data="provizor_order_done_list")
    button3 = types.InlineKeyboardButton(
        text="Особистий кабінет", callback_data="provizor_personal_account")
    button4 = types.InlineKeyboardButton(
        text="Інформація про бота", callback_data="provizor_about")
    keyboard.add(button1, button2, button3, button4, row_width=1)
    return keyboard


def back_to_main_menu():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text="Повернутись до головного меню", callback_data="user_main_menu")
    keyboard.add(button)
    return keyboard


def list_keyboard(l):
    #l = ['Яблоко', 'Груша']
    keyboard = types.InlineKeyboardMarkup()
    backbutton = types.InlineKeyboardButton(
        text="Повернутись до головного меню", callback_data="user_main_menu")
    button_list = [types.InlineKeyboardButton(
        text=x, callback_data="user_medicine_list|"+x) for x in l]
    keyboard.add(*button_list, backbutton, row_width=1)
    return keyboard


def list_order_keyboard(l):
    """ Клавіатура-список замовлень для провізора """
    keyboard = types.InlineKeyboardMarkup()
    backbutton = types.InlineKeyboardButton(
        text="Повернутись до головного меню", callback_data="provizor_main_menu")
    button_list = [types.InlineKeyboardButton(
        text=x, callback_data="provizor_order_list|"+x) for x in l]
    keyboard.add(*button_list, backbutton, row_width=1)
    return keyboard


def user_list_order_keyboard(l):
    """ Клавіатура-список замовлень для провізора """
    keyboard = types.InlineKeyboardMarkup()
    backbutton = types.InlineKeyboardButton(
        text="Повернутись до головного меню", callback_data="user_main_menu")
    button_list = [types.InlineKeyboardButton(
        text=x, callback_data="user_order_list|"+x) for x in l]
    keyboard.add(*button_list, backbutton, row_width=1)
    return keyboard


def list_order_done_keyboard(l):
    """ Клавіатура-список виконаних замовлень для провізора """
    #l = ['Яблоко', 'Груша']
    keyboard = types.InlineKeyboardMarkup()
    backbutton = types.InlineKeyboardButton(
        text="Повернутись до головного меню", callback_data="provizor_main_menu")
    button_list = [types.InlineKeyboardButton(
        text=x, callback_data="provizor_order_done_list|"+x) for x in l]
    keyboard.add(*button_list, backbutton, row_width=1)
    return keyboard


def keyboard_main_menu_provizor():
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text="Переглянути список ліків", callback_data="medicine_list")
    button2 = types.InlineKeyboardButton(
        text="Переглянути замовлення", callback_data="order_medicine")
    button3 = types.InlineKeyboardButton(
        text="Особистий кабінет", callback_data="personal_account")
    button4 = types.InlineKeyboardButton(
        text="Інформація про бота", callback_data="about")

    keyboard.add(button1, button2, button3, button4, row_width=1)
    return keyboard


def back_to_main_menu_provizor():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text="Повернутись до головного меню", callback_data="provizor_main_menu")
    keyboard.add(button)
    return keyboard


def back_to_order_list():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text="Повернутись до списку замовлень", callback_data="provizor_order_list")
    keyboard.add(button)
    return keyboard


def keyboard_yes_no():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=(True),
                                         row_width=2,
                                         one_time_keyboard=(True))
    button1 = types.KeyboardButton("Так")
    button2 = types.KeyboardButton("Ні")
    keyboard.add(button1, button2)
    return keyboard


def clear_keyboard():
    return types.ReplyKeyboardRemove()


def keyboard_doctor_main_menu():
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text="Виписати рецепт", callback_data="doctor_write_prescription")
    button2 = types.InlineKeyboardButton(
        text="Особистий кабінет", callback_data="doctor_personal_account")
    button3 = types.InlineKeyboardButton(
        text="Інформація про бота", callback_data="doctor_about")
    keyboard.add(button1, button2, button3, row_width=1)
    return keyboard


def list_med_doctor_keyboard(l):
    #l = ['Яблоко', 'Груша']
    keyboard = types.InlineKeyboardMarkup()
    backbutton = types.InlineKeyboardButton(
        text="Повернутись до головного меню", callback_data="doctor_main_menu")
    button_list = [types.InlineKeyboardButton(
        text=x, callback_data="doctor_medicament_list|"+x) for x in l]
    keyboard.add(*button_list, backbutton, row_width=1)
    return keyboard


def back_to_main_menu_doctor():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text="Повернутись до головного меню", callback_data="doctor_main_menu")
    keyboard.add(button)
    return keyboard


def keyboard_back():
    """Повернутись до головного меню"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=(True),
                                         one_time_keyboard=(True))
    button = types.KeyboardButton("Повернутись до головного меню")
    keyboard.add(button)
    return keyboard
