# -*- coding: utf-8 -*-

import telebot
from telebot import types

import config
import database
import registration
import login
import user_workspace
import provizor_workspace
import doctor_workspace


bot = telebot.TeleBot(config.config["token"],
                      skip_pending=(True), threaded=(False))


@bot.message_handler(commands=["start"])
def start_chat(message):
    """
    Ця функція виконується при введенні команди /start .
    Відбувається авторизація або реєстрація користувача.
    """
    try:
        bot.delete_message(message.chat.id, message.message_id - 1)
        # bot.clear
    except:
        pass
    if database.user_verification(message.chat.id):
        # автоматична авторизація через chat.id (primary key in `client`)
        if (
            database.operation_users(
                "SELECT is_provizor FROM users where id = " +
                str(message.chat.id) + ";"
            )
            == "1"
        ):
            # вхід провізора
            bot.send_message(message.chat.id, "Вхід виконано")
            provizor_workspace.start_workspace(message, bot)
        elif (
            database.operation_users(
                "SELECT is_doctor FROM users where id = " +
                str(message.chat.id) + ";"
            )
            == "1"
        ):
            # вхід лікаря
            bot.send_message(message.chat.id, "Вхід виконано")
            doctor_workspace.start_workspace(message, bot)
        else:
            # вхід користувача
            bot.send_message(
                message.chat.id,
                "Вас вітає pharmacy-bot! Ви вже ввійшли в систему"
            )
            user_workspace.start_workspace(message, bot)
    else:
        # меню реєстрації / входу
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


@bot.message_handler(commands=["info"])
def info(message):
    bot.send_message(
        message.chat.id,
        "Якщо виникла якась помилка, то радимо перезапустити бота командою /start",
    )


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        # нижче відбувається розділення одного аргументу на 2
        # (якщо такий аргумент був переданий)
        first_param = call.data.split("|")[0]
        second_param = call.data.split("|")[1]

        if first_param == "user_medicine_list":
            # показ медикаменту із списку для користувача
            bot.delete_message(call.message.chat.id, call.message.message_id)
            user_workspace.choose_medicine(call.message, bot, second_param)
        elif first_param == "user_show_medicine":
            # показ інформації про препарат
            bot.delete_message(call.message.chat.id, call.message.message_id)
            user_workspace.order_medicine(call.message, bot, second_param)
        elif first_param == "provizor_order_done":
            # виведення результат виконання замовлення для провізора
            bot.delete_message(call.message.chat.id, call.message.message_id)
            provizor_workspace.order_medicine(call.message, bot, second_param)
        elif first_param == "provizor_order_done_list":
            # показ інформації про виконане замовлення для провізора
            bot.delete_message(call.message.chat.id, call.message.message_id)
            provizor_workspace.choose_order_done(
                call.message, bot, second_param)
        elif first_param == "provizor_order_list":
            # показ інформації про замовлення для провізора
            bot.delete_message(call.message.chat.id, call.message.message_id)
            provizor_workspace.choose_order(call.message, bot, second_param)
        elif first_param == "user_order_list":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            user_workspace.choose_order(call.message, bot, second_param)
        elif first_param == "doctor_medicament_list":
            # виведення інформація про медикамент для лікаря
            bot.delete_message(call.message.chat.id, call.message.message_id)
            doctor_workspace.choose_medicine(call.message, bot, second_param)
        elif first_param == "doctor_enter_medicine":
            # початок створення рецепту
            bot.delete_message(call.message.chat.id, call.message.message_id)
            doctor_workspace.write_prs_step_2(call.message, bot, second_param)
    except:

        # якщо не було знайдено символу поділу аргумента '|':
        if call.data == "2":
            # реєстрація користувача
            bot.delete_message(call.message.chat.id, call.message.message_id)
            msg = bot.send_message(
                call.message.chat.id,
                "Реєстрація користувача.\nНадішліть свою пошту"
            )
            bot.register_next_step_handler(msg, registration.registration, bot)
        elif call.data == "1":
            # авторизація користувача
            bot.delete_message(call.message.chat.id, call.message.message_id)
            msg = bot.send_message(call.message.chat.id,
                                   "Вхід\nНадішліть свою пошту")
            bot.register_next_step_handler(msg, login.user_authorization, bot)
        elif call.data == "user_main_menu":
            # виведення меню для користувача
            bot.delete_message(call.message.chat.id, call.message.message_id)
            user_workspace.start_workspace(call.message, bot)
        elif call.data == "provizor_main_menu":
            # виведення меню для фармацевта
            bot.delete_message(call.message.chat.id, call.message.message_id)
            provizor_workspace.start_workspace(call.message, bot)
        elif call.data == "user_medicine_list":
            #  виведення списку ліків для користувача
            bot.delete_message(call.message.chat.id, call.message.message_id)
            user_workspace.medicine_list(call.message, bot)
        elif call.data == "provizor_order_list":
            # виведення списку замовлень для провізора
            bot.delete_message(call.message.chat.id, call.message.message_id)
            provizor_workspace.order_list(call.message, bot)
        elif call.data == "provizor_order_done_list":
            # виведення списку виконаних замовлень для провізора
            bot.delete_message(call.message.chat.id, call.message.message_id)
            provizor_workspace.order_done_list(call.message, bot)
        elif call.data == "doctor_main_menu":
            # виведення меню для лікаря
            bot.delete_message(call.message.chat.id, call.message.message_id)
            doctor_workspace.start_workspace(call.message, bot)
        elif call.data == "doctor_write_prescription":
            # виписування рецепту
            bot.delete_message(call.message.chat.id, call.message.message_id)
            doctor_workspace.write_prescription(call.message, bot)
        elif call.data == "user_order":
            #
            bot.delete_message(call.message.chat.id, call.message.message_id)
            user_workspace.order_list(call.message, bot)
        elif call.data == "user_personal_account":
            # інформація про користувача
            bot.delete_message(call.message.chat.id, call.message.message_id)
            user_workspace.personal_account(call.message, bot)
        elif call.data == "provizor_personal_account":
            # інформація про провізора
            bot.delete_message(call.message.chat.id, call.message.message_id)
            provizor_workspace.personal_account(call.message, bot)
        elif call.data == "doctor_personal_account":
            # інформація про лікаря
            bot.delete_message(call.message.chat.id, call.message.message_id)
            doctor_workspace.personal_account(call.message, bot)
        elif call.data == "user_about":
            # інформація про бота
            bot.delete_message(call.message.chat.id, call.message.message_id)
            user_workspace.about(call.message, bot)
        elif call.data == "provizor_about":
            # інформація про бота
            bot.delete_message(call.message.chat.id, call.message.message_id)
            provizor_workspace.about(call.message, bot)
        elif call.data == "doctor_about":
            # інформація про бота
            bot.delete_message(call.message.chat.id, call.message.message_id)
            doctor_workspace.about(call.message, bot)


# запуск бота
bot.polling(none_stop=True, interval=1, timeout=120)
