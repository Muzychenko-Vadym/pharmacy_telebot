# -*- coding: utf-8 -*-
"""
Цей файл містить функції, необхідні для
авторизації користувача
"""

import re

import database
import hash_password
import user_workspace
from telebot import types


def user_authorization(message, bot):
    if (re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)", message.text.lower())):
        user_email = message.text
        msg = bot.send_message(message.chat.id, "Введіть пароль")
        bot.register_next_step_handler(msg, aut_step_1, bot, user_email)
    else:
        msg2 = bot.send_message(
            message.chat.id,
            "Поштова скринька не має містити заборонених символів. Надішліть свою пошту")
        bot.register_next_step_handler(msg2, user_authorization, bot)


def aut_step_1(message, bot, user_email):
    user_password = message.text
    user_hashed_pass = str(
        database.user_autorization(user_email))
    if(hash_password.check_password(user_hashed_pass, user_password)):

        old_id = database.select_operation(
            "SELECT id FROM `client` WHERE email = '"+str(user_email)+"';")
        database.user_autorization_id_update(
            user_email,
            message.chat.id,
            old_id
        )
        bot.send_message(message.chat.id, "Вхід виконано")
        user_workspace.start_workspace(message, bot)
    else:
        bot.send_message(
            message.chat.id,
            "Введено невірну поштову скриньку або невірний пароль. Спробуйте ввести заново")
        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton(text="Увiйти", callback_data="1")
        itembtn2 = types.InlineKeyboardButton(
            text="Зареєструватись", callback_data="2")
        markup.add(itembtn1, itembtn2, row_width=1)
        bot.send_message(
            message.chat.id,
            "Вас вітає pharmacy-bot! Увійдіть або зареєструйтесь у системі",
            reply_markup=markup,
        )
