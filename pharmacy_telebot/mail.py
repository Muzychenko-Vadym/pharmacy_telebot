# -*- coding: utf-8 -*-
"""
Цей файл містить функції відправки повідомлення на пошту
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_to_email(email, rnd_code):
    addr_from = "pharmacy.test.bot@gmail.com"
    addr_to = str(email)
    password = "Afdh3k2i6"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = 'Реєстрація'

    body = "Код підтвердження: "+str(rnd_code)
    print(body)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.set_debuglevel(True)
    server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()
