from flask_restful import Resource
from flask import Flask
from flask_restful import Api
import random
from flask import request, redirect, url_for, send_file
from pymysql.cursors import DictCursor
from contextlib import closing
from hashlib import sha256
from flask import render_template
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required
from datetime import datetime
import time
import pymysql
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version
from flask import Response
import excel_history
import re

app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]
app.config['JWT_BLACKLIST_ENABLED'] = True
jwt = JWTManager(app)
app.config['PROPAGATE_EXCEPTIONS'] = True

def insert_to_register(message, mode):
    with closing(pymysql.connect(host="localhost", user="b92599ho_ivr", password="gQz6g3H*", db="b92599ho_ivr",
                                 charset="utf8", use_unicode=True, cursorclass=DictCursor)) as connection:
        with connection.cursor() as cursor:
            if mode == 'check_tokens': #проверка на то, чтобы токены пользователя не истекли на текущий момент времени
                user_table = cursor.execute(
                    "SELECT * FROM `JWT` WHERE `access_token`='{}'".format(message["access_token"]))
                if user_table != 0:
                    f = "SELECT `user_id` FROM `JWT` WHERE `access_token`='{}'".format(message['access_token'])
                    cursor.execute(f)
                    id_find = cursor.fetchall()
                    id = (str(id_find[0]['user_id']))
                    f = "SELECT `token` FROM `users` WHERE `id`='{}'".format(id)
                    cursor.execute(f)
                    token = cursor.fetchall()
                    access_token = create_access_token(identity=token)
                    refresh_token = create_access_token(identity=token)

                    current_datetime = str(datetime.now())
                    time1 = int(
                        time.mktime(time.strptime(current_datetime[:len(current_datetime) - 7], '%Y-%m-%d %H:%M:%S')))
                    string = "SELECT `refresh_token_time` FROM `JWT` WHERE `refresh_token`='" + message[
                        "refresh_token"] + "'"
                    cursor.execute(string)
                    deltatime = cursor.fetchall()
                    time2 = int(time.mktime(time.strptime(deltatime[0]['refresh_token_time'], '%Y-%m-%d %H:%M:%S')))
                    if (time1 - time2) > 2592000:
                        user_table = "UPDATE `JWT` SET `refresh_token_time`='" + current_datetime[:len(
                            current_datetime) - 7] + "' ,`refresh_token`='" + refresh_token + "' WHERE `user_id`='" + id + "'"
                        cursor.execute(user_table)
                        connection.commit()

                    string = "SELECT `access_token_time` FROM `JWT` WHERE `access_token`='{}'".format(
                        message["access_token"])
                    cursor.execute(string)
                    deltatime = cursor.fetchall()
                    time2 = int(time.mktime(time.strptime(deltatime[0]['access_token_time'], '%Y-%m-%d %H:%M:%S')))
                    if (time1 - time2) > 850:
                        user_table = "UPDATE `JWT` SET `access_token_time`='" + current_datetime[:len(
                            current_datetime) - 7] + "' ,`access_token`='" + access_token + "' WHERE `user_id`='" + id + "'"
                        cursor.execute(user_table)
                        connection.commit()
                        result_access_token = access_token
                    else:
                        result_access_token = message["access_token"]

                else:
                    user_table = cursor.execute(
                        "SELECT * FROM `JWT` WHERE `refresh_token`='{}'".format(message["refresh_token"]))
                    if user_table != 0:
                        f = "SELECT `user_id` FROM `JWT` WHERE `refresh_token`='{}'".format(message["refresh_token"])
                        cursor.execute(f)
                        id_find = cursor.fetchall()
                        id = (str(id_find[0]['user_id']))
                        f = "SELECT `token` FROM `users` WHERE `id`='{}'".format(id)
                        cursor.execute(f)
                        token = cursor.fetchall()
                        access_token = create_access_token(identity=token)
                        refresh_token = create_access_token(identity=token)

                        current_datetime = str(datetime.now())
                        time1 = int(time.mktime(
                            time.strptime(current_datetime[:len(current_datetime) - 7], '%Y-%m-%d %H:%M:%S')))

                        string = "SELECT `refresh_token_time` FROM `JWT` WHERE `refresh_token`='" + message[
                            "refresh_token"] + "'"
                        cursor.execute(string)
                        deltatime = cursor.fetchall()
                        time2 = int(time.mktime(time.strptime(deltatime[0]['refresh_token_time'], '%Y-%m-%d %H:%M:%S')))
                        if (time1 - time2) > 2592000:
                            user_table = "UPDATE `JWT` SET `refresh_token_time`='" + current_datetime[:len(
                                current_datetime) - 7] + "' ,`refresh_token`='" + refresh_token + "' WHERE `user_id`='" + id + "'"
                            cursor.execute(user_table)
                            connection.commit()

                        string = "SELECT `access_token_time` FROM `JWT` WHERE `refresh_token`='{}'".format(
                            message["refresh_token"])
                        cursor.execute(string)
                        deltatime = cursor.fetchall()
                        time2 = int(time.mktime(time.strptime(deltatime[0]['access_token_time'], '%Y-%m-%d %H:%M:%S')))
                        if (time1 - time2) > 850:
                            user_table = "UPDATE `JWT` SET `access_token_time`='" + current_datetime[:len(
                                current_datetime) - 7] + "' ,`access_token`='" + access_token + "' WHERE `user_id`='" + id + "'"
                            cursor.execute(user_table)
                            connection.commit()
                            result_access_token = access_token
                        else:
                            f = "SELECT `access_token` FROM `JWT` WHERE `refresh_token`='{}'".format(
                                message["refresh_token"])
                            cursor.execute(f)
                            access_token = cursor.fetchall()
                            result_access_token = access_token[0]['access_token']
                    else:
                        return "plsenter"
                return {"id": id, "result_access_token": result_access_token}

            if mode == 'reg': #регистрация
                if message['email'] == '' or message['password'] == '' or message['name'] == '': return "notallowed"
                if not check_name(message['name']): return "invname"
                if not check_email(message['email']): return "invemail"
                message['name'] = word_processing(message['name'])
                user_table = cursor.execute("select * from users where email=%s", message['email'])
                if user_table == 0:
                    if check_password(message['password']):
                        token = Hash(message['email'] + message['password'])
                        query = "INSERT INTO `users` (`id`, `name`,`email`, `token`) VALUES (NULL,'" + message[
                            'name'] + "', '" + message['email'] + "', '" + token + "')"
                        cursor.execute(query)
                        connection.commit()
                        access_token = create_access_token(identity=token)
                        refresh_token = create_refresh_token(identity=token)
                        current_datetime = str(datetime.now())
                        f = "SELECT `id` FROM `users` WHERE `token`='{}'".format(token)
                        cursor.execute(f)
                        id_find = cursor.fetchall()
                        query = "INSERT INTO `JWT` (`user_id`, `access_token` , `access_token_time`, `refresh_token` , `refresh_token_time`) VALUES ( '" + str(
                            id_find[0]['id']) + "', '" + access_token + "','" + current_datetime[:len(
                            current_datetime) - 7] + "','" + refresh_token + "','" + current_datetime[
                                                                                     :len(current_datetime) - 7] + "')"
                        cursor.execute(query)
                        connection.commit()

                        return {'access_token': access_token, 'refresh_token': refresh_token}
                    else:
                        return "invpassword"
                else:
                    return "dublicate"
            elif mode == 'ent': #вход
                if message['email'] == '' or message['password'] == '': return "notallowed"
                token = Hash(message['email'] + message['password'])
                user_table = cursor.execute("select * from users where token=%s", token)
                if user_table != 0:
                    access_token = create_access_token(identity=token)
                    refresh_token = create_refresh_token(identity=token)
                    current_datetime = str(datetime.now())
                    f = "SELECT `id` FROM `users` WHERE `token`='{}'".format(token)
                    cursor.execute(f)
                    id_find = cursor.fetchall()
                    user_table = cursor.execute("SELECT * FROM `JWT` WHERE user_id = '{}'".format(
                        str(id_find[0]['id'])))
                    if user_table == 0:
                        query = "INSERT INTO `JWT` (`user_id`, `access_token` , `access_token_time`, `refresh_token` , `refresh_token_time`) VALUES ( '" + str(
                            id_find[0]['id']) + "', '" + access_token + "','" + current_datetime[:len(
                            current_datetime) - 7] + "', '" + refresh_token + "','" + current_datetime[
                                                                                      :len(current_datetime) - 7] + "')"
                    else:
                        query = "UPDATE `JWT` SET `access_token`=" + "'" + access_token + "'" + " , `access_token_time`=" + "'" + current_datetime[:len(current_datetime) - 7] + "' WHERE `user_id` ='" + str(id_find[0]['id']) + "'"
                    cursor.execute(query)
                    connection.commit()
                    string = "SELECT `refresh_token` FROM `JWT` WHERE `user_id`='" + str(id_find[0]['id']) + "'"
                    cursor.execute(string)
                    refresh_token = cursor.fetchall()
                    return {'access_token': access_token, 'refresh_token': refresh_token[0]['refresh_token']}
                else:
                    return "notfound"
            elif mode == "info-lk": #получение информации профиля пользователя
                result = insert_to_register(message, "check_tokens")
                if result == "plsenter":
                    return "plsenter"
                else:
                    id = result['id']
                    result_access_token = result['result_access_token']
                    f = "SELECT `md_number`, `your_business`, `conc_business`, `radius`, `stopped_points_adress`, `stopped_points_coords`, `time` FROM `requests_history` WHERE `user_id` = '" + id + "'"
                    cursor.execute(f)
                    data = cursor.fetchall()
                    user_table = cursor.execute("SELECT * FROM `requests_history` WHERE `user_id` = '" + id + "'")
                    keys = []
                    for i in range(1, user_table + 1): keys.append(str(i))
                    excel_history.WriteIn(dict(zip(keys, data)), id)

                    string = "SELECT `email`, `name`,`token`,`isEmailConfirmed` FROM `users` WHERE `id`='{}'".format(id)
                    cursor.execute(string)
                    fullstring = cursor.fetchall()
                    return {'id': id, 'user_info': fullstring[0], 'access_token': result_access_token}

            elif mode == "cng": #изменение информации профиля пользователя
                if message['curr_email'] == message['email']: return "sameemail1"
                if message['curr_name'] == message['name']: return "samename"
                message['name'] = word_processing(message['name'])
                user_table = cursor.execute("select * from users where email=%s", message['email'])
                if user_table == 0:
                    f = "SELECT `id` FROM `users` WHERE `email`='{}'".format(message['curr_email'])
                    cursor.execute(f)
                    id_find = cursor.fetchall()
                    id = (str(id_find[0]['id']))
                    f1 = CheckChangingInformation(message, id)
                    if f1 != "notchanged" and f1 != "invpassword" and f1 != "invemail" and f1 != "samepass" and f1 != "invname":
                        cursor.execute(f1)
                        connection.commit()
                        if message['password'] != "":
                            query = "DELETE FROM `JWT` WHERE `user_id` = '" + id + "'"
                            cursor.execute(query)
                            connection.commit()
                        return "changed"
                    else:
                        return CheckChangingInformation(message, id)
                else:
                    return "sameemail"

            elif mode == "sendmessage": #отправка сообщения по футеру
                server = 'smtp.gmail.com'
                user = 'montesume@gmail.com'
                password = 'xdazalszusfsdyzj'
                recipients = 'montesume@gmail.com'
                sender = 'montesume@gmail.com'
                if not check_name(message['name']): return "invname"
                if not check_email(message['email']): return "invemail"
                subject = "Сообщение от пользователя " + message['name'] + ": " + message['email']
                text = "<h3 style ='font-size: 20px; color: #000; margin-top:10px;'><b>" + message['text'] + "</b></h3>"
                html = '<html><head></head><body><p>' + text + '</p></body></html>'
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = recipients
                msg['Reply-To'] = sender
                msg['Return-Path'] = sender
                msg['X-Mailer'] = 'Python/' + (python_version())
                part_text = MIMEText(text, 'plain')
                part_html = MIMEText(html, 'html')
                msg.attach(part_text)
                msg.attach(part_html)
                mail = smtplib.SMTP_SSL(server)
                mail.login(user, password)
                mail.sendmail(sender, recipients, msg.as_string())
                mail.quit()
                return "success"
            elif mode == "sendconfirm": #отправка кода подтверждения
                f = "SELECT `user_id` FROM `JWT` WHERE `access_token`='{}'".format(message['access_token'])
                cursor.execute(f)
                id_find = cursor.fetchall()
                id = (str(id_find[0]['user_id']))
                code = str(random.randint(100001, 999999))
                query = "DELETE FROM `CODE` WHERE `user_id`='" + id + "'"
                cursor.execute(query)
                connection.commit()

                user_table = cursor.execute("SELECT * FROM `CODE` WHERE user_id = '" + id + "'")
                if user_table == 0:
                    query = "INSERT INTO `CODE` (`user_id`, `access_token` , `confirmcode`) VALUES ( '" + id + "', '" + \
                            message['access_token'] + "','" + code + "')"
                else:
                    query = "UPDATE `CODE` SET `confirmcode`=" + "'" + code + "'" + " , `access_token`=" + "'" + \
                            message['access_token'] + "' WHERE `user_id` ='" + id + "'"

                cursor.execute(query)
                connection.commit()
                server = 'smtp.gmail.com'
                user = 'montesume@gmail.com'
                password = 'xdazalszusfsdyzj'
                recipients = message['email']
                sender = 'montesume@gmail.com'
                subject = 'Код подтверждения email на Montesume - ' + code
                text = "<h3 style ='font-size: 20px; color: #000;'><b>Здравсвуйте!</b></h3>" \
                       "<h3  style ='margin-top:30px;'>Ваш код подтверждения - <b style ='color: #FF914D'>" + code + "</b></h3>" \
                                                                                                                     "<h3 style = 'margin-top:30px;'> С уважением, " \
                                                                                                                     "<h3 style = 'margin-top:20px;'> Montesume" \
                                                                                                                     "<h3 style = 'color: #777777;font-size:12px; margin-top:20px;'> Это письмо сформировано автоматически и не требует ответа."
                html = '<html><head></head><body><p>' + text + '</p></body></html>'
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = recipients
                msg['Reply-To'] = sender
                msg['Return-Path'] = sender
                msg['X-Mailer'] = 'Python/' + (python_version())
                part_text = MIMEText(text, 'plain')
                part_html = MIMEText(html, 'html')
                msg.attach(part_text)
                msg.attach(part_html)
                mail = smtplib.SMTP_SSL(server)
                mail.login(user, password)
                mail.sendmail(sender, recipients, msg.as_string())
                mail.quit()
                return "message_email"
            elif mode == "checkconfirm": #получение самого кода подтвердждения
                result = insert_to_register(message, "check_tokens")
                if result == "plsenter":
                    return "plsenter"
                else:
                    id = result['id']
                    result_access_token = result['result_access_token']
                    query = "UPDATE `CODE` SET `access_token`='" + result_access_token + "' WHERE `user_id`=" + id
                    cursor.execute(query)
                    connection.commit()
                    user_table = "SELECT `confirmcode` FROM `CODE` WHERE `access_token`='" + result_access_token + "'"
                    cursor.execute(user_table)
                    code = cursor.fetchall()
                    return code[0]['confirmcode']
            elif mode == "successconfirm": #осуществление успешного подтверждения чего-либо
                result = insert_to_register(message, "check_tokens")
                if result == "plsenter":
                    return "plsenter"
                else:
                    id = result['id']
                    user_table = "UPDATE `users` SET `isEmailConfirmed`=1 WHERE `id`='" + id + "'"
                    cursor.execute(user_table)
                    connection.commit()
                    return "success"
            elif mode == 'makehisreq': #формирование истории запросов
                result = insert_to_register(message, "check_tokens")
                if result == "plsenter":
                    return "plsenter"
                else:
                    id = result['id']

                    user_table = cursor.execute(
                        "SELECT * FROM `requests_history` WHERE `user_id`='" + id + "' AND `your_business`='" + mas_processing(
                            message['your_business']) + "' AND `conc_business`='" + mas_processing(
                            message['concurent_business']) + "' AND `radius`='" + str(
                            message['radius']) + "' AND `stopped_points_adress`='" + mas_processing(
                            message['stopped_points_adresses']) + "' AND `stopped_points_coords`='" + mas_processing(
                            message['stopped_points_coords']) + "'")
                    if user_table > 0: return "samerequest"

                    current_datetime = str(datetime.now())
                    query = "INSERT INTO `requests_history` (`user_id`, `access_token`, `md_number`, `your_business`, `conc_business`, `radius`, `stopped_points_adress`, `stopped_points_coords`, `time`)" \
                            " VALUES ('" + str(id) + "', '" + str(message['access_token']) + "', '" + str(
                        message['md_number']) + "', '" + mas_processing(
                        message['your_business']) + "', '" + mas_processing(
                        message['concurent_business']) + "', '" + str(message['radius']) + "', '" + mas_processing(
                        message['stopped_points_adresses']) + "', '" + mas_processing(
                        message['stopped_points_coords']) + "', '" + current_datetime[:len(current_datetime) - 7] + "')"
                    cursor.execute(query)
                    connection.commit()
                    return "saved"
            elif mode == 'showhisreq': #получение истории запросов для её дальнейшего отображения пользователю
                result = insert_to_register(message, "check_tokens")
                if result == "plsenter":
                    return "plsenter"
                else:
                    id = result['id']
                    f = "SELECT `md_number`, `your_business`, `conc_business`, `radius`, `stopped_points_adress`, `stopped_points_coords`, `time` FROM `requests_history` WHERE `user_id` = '" + id + "'"
                    cursor.execute(f)
                    data = cursor.fetchall()
                    user_table = cursor.execute("SELECT * FROM `requests_history` WHERE `user_id` = '" + id + "'")
                    keys = []
                    for i in range(1, user_table + 1): keys.append(str(i))
                    return dict(zip(keys, data))
            elif mode == "delhisreq": #очищение истории запросов
                result = insert_to_register(message, "check_tokens")
                if result == "plsenter":
                    return "plsenter"
                else:
                    id = result['id']
                    f = "DELETE FROM `requests_history` WHERE `user_id` =" + id
                    cursor.execute(f)
                    connection.commit()
                    return "deleted"
            elif mode == "passrecover": #восстановление пароля
                if not check_email(message['email']): return "notallowed"
                newpassword = ""
                for i in range(16):
                    if i <= 10:
                        x = random.randint(1, 2)
                        if x == 1:
                            newpassword += chr(random.randint(65, 90))
                        elif x == 2:
                            newpassword += chr(random.randint(97, 122))
                    else:
                        newpassword += chr(random.randint(48, 57))
                f = "SELECT `id` FROM `users` WHERE `email`='{}'".format(message['email'])
                cursor.execute(f)
                if cursor.execute(f) == 0: return "notfound"
                id_find = cursor.fetchall()
                id = (str(id_find[0]['id']))
                query = "DELETE FROM `JWT` WHERE `user_id` = '" + id + "'"
                cursor.execute(query)
                connection.commit()
                f = "SELECT `email` FROM `users` WHERE `id`='" + id + "'"
                cursor.execute(f)
                curremail = cursor.fetchall()[0]["email"]
                token = Hash(curremail + newpassword)
                query = "UPDATE `users` SET `token`='" + token + "' WHERE `id`=" + id
                cursor.execute(query)
                connection.commit()
                server = 'smtp.gmail.com'
                user = 'montesume@gmail.com'
                password = 'xdazalszusfsdyzj'
                recipients = message['email']
                sender = 'montesume@gmail.com'
                subject = 'Ваш новый пароль на Montesume - ' + newpassword
                text = "<h3 style ='font-size: 20px; color: #000;'><b>Здравсвуйте!</b></h3>" \
                       "<h3  style ='margin-top:30px;'>Ваш новый пароль - <b style ='color: #FF914D'>" + newpassword + "</b></h3>" \
                                                                                                                       "<h3 style = 'margin-top:30px;'> С уважением, " \
                                                                                                                       "<h3 style = 'margin-top:20px;'> Montesume" \
                                                                                                                       "<h3 style = 'color: #777777;font-size:12px; margin-top:20px;'> Это письмо сформировано автоматически и не требует ответа."
                html = '<html><head></head><body><p>' + text + '</p></body></html>'
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = recipients
                msg['Reply-To'] = sender
                msg['Return-Path'] = sender
                msg['X-Mailer'] = 'Python/' + (python_version())
                part_text = MIMEText(text, 'plain')
                part_html = MIMEText(html, 'html')
                msg.attach(part_text)
                msg.attach(part_html)
                mail = smtplib.SMTP_SSL(server)
                mail.login(user, password)
                mail.sendmail(sender, recipients, msg.as_string())
                mail.quit()
                return "send"
            elif mode == "downloadhisreq": #скачивание истории запросов
                result = insert_to_register(message, "check_tokens")
                if result == "plsenter":
                    return "plsenter"
                else:
                    id = result['id']
                    f = "SELECT `md_number`, `your_business`, `conc_business`, `radius`, `stopped_points_adress`, `stopped_points_coords`, `time` FROM `requests_history` WHERE `user_id` = '" + id + "'"
                    cursor.execute(f)
                    data = cursor.fetchall()
                    user_table = cursor.execute("SELECT * FROM `requests_history` WHERE `user_id` = '" + id + "'")
                    keys = []
                    for i in range(1, user_table + 1): keys.append(str(i))
                    excel_history.WriteIn(dict(zip(keys, data)))
                    return "success"

#хеширование почты+пароля пользователя
def Hash(input):
    return sha256(input.encode('utf-8')).hexdigest()

#проверка правильности ввода ФИО
def check_name(name):
    pattern1 = r"[А-ЯЁ][а-яё\-]+\s+[А-ЯЁ][а-яё\-]+\s+[А-ЯЁ][а-яё\-]"
    pattern2 = r"[A-Z][a-z\-]+\s+[A-Z][a-z\-]+\s+[A-Z][a-z\-]"
    if re.search('\d+', name) is None:
        if re.match(pattern1, name) is not None or re.match(pattern2, name) is not None:
            return True
    return False

#проверка правильности ввода email
def check_email(email):
    pattern = r"([A-Z0-9a-z._-]+)@([A-Za-z0-9.-]+\.[a-z]{2,})"
    if re.match(pattern, email) is not None:
        return True
    else:
        return False

#проверка правильности ввода пароля
def check_password(password):
    return not (
                len(password) < 6 or password.isdigit() or password.isalpha() or password.islower() or password.isupper()) and password.isalnum()

#осуществление изменения информации профиля пользователя
def CheckChangingInformation(message, id):
    if message['name'] == "" and message['email'] == "" and message['password'] == "":
        return '''notchanged'''
    elif message['name'] != "" and message['email'] == "" and message['password'] == "":
        if not check_name(message['name']): return "invname"
        return "UPDATE `users` SET `name`='" + message['name'] + "' WHERE `id`=" + id
    elif message['name'] == "" and message['email'] != "" and message['password'] == "":
        if not check_email(message['email']): return "invemail"
        return "UPDATE `users` SET `email`='" + message['email'] + "' WHERE `id`=" + id
    elif message['name'] == "" and message['email'] == "" and message['password'] != "":
        if not check_password(message['password']): return "invpassword"
        token = Hash(message['curr_email'] + message['password'])
        if message['curr_token'] == token: return "samepass"
        return "UPDATE `users` SET `token`='" + token + "' WHERE `id`=" + id
    elif message['name'] != "" and message['email'] != "" and message['password'] == "":
        if not check_name(message['name']): return "invname"
        if not check_email(message['email']): return "invemail"
        return "UPDATE `users` SET `email`='" + message['email'] + "', `name`='" + message[
            'name'] + "' WHERE `id`=" + id
    elif message['name'] != "" and message['email'] == "" and message['password'] != "":
        if not check_name(message['name']): return "invname"
        if not check_password(message['password']): return "invpassword"
        token = Hash(message['curr_email'] + message['password'])
        if message['curr_token'] == token: return "samepass"
        return "UPDATE `users` SET `name`='" + message['name'] + "', `token`='" + token + "' WHERE `id`=" + id
    elif message['name'] == "" and message['email'] != "" and message['password'] != "":
        if not check_email(message['email']): return "invemail"
        if not check_password(message['password']): return "invpassword"
        token = Hash(message['curr_email'] + message['password'])
        if message['curr_token'] == token: return "samepass"
        token = Hash(message['email'] + message['password'])
        return "UPDATE `users` SET `email`='" + message['email'] + "', `token`='" + token + "' WHERE `id`=" + id
    elif message['name'] != "" and message['email'] != "" and message['password'] != "":
        if not check_name(message['name']): return "invname"
        if not check_email(message['email']): return "invemail"
        if not check_password(message['password']): return "invpassword"
        token = Hash(message['curr_email'] + message['password'])
        if message['curr_token'] == token: return "samepass"
        token = Hash(message['email'] + message['password'])
        return "UPDATE `users` SET `email`='" + message['email'] + "', `token`='" + token + "', `name`='" + message[
            'name'] + "' WHERE `id`=" + id

#обработка массива при формировании истории запросов
def mas_processing(mas):
    result = ''
    for i in range(len(mas)):
        if i != len(mas) - 1:
            result += word_processing(str(mas[i])) + ', '
        else:
            result += word_processing(str(mas[i]))
    return result

#обработка нужного слова для удаления лишних пробелов
def word_processing(word):
    while "  " in word:
        word = word.replace("  ", " ")
    return word

#осуществление регистрации
class UserRegistration(Resource):
    def post(self):
        return {"result": insert_to_register(request.json, 'reg')}

    def get(self):
        return Response(render_template("register.html"))

#осуществление входа
class UserLogin(Resource):
    def post(self):
        return {"result": insert_to_register(request.json, 'ent')}

    def get(self):
        return Response(render_template("enter.html"))

#осуществление восстановления пароля
class UserPasswordRecover(Resource):
    def post(self):
        return {"result": insert_to_register(request.json, 'passrecover')}

    def get(self):
        return Response(render_template("passwordrecover.html"))

#отправка файла страницы личного кабинета
class UserLK(Resource):
    def get(self):
        return send_file("templates/pr_office.html")

#получение информации профиля пользователя
class UserInformation(Resource):
    def get(self):
        return {"1": request.headers['Authorization'][7:], "2": request.headers['evrica_refresh_token']}

    def post(self):
        return insert_to_register(request.json, 'info-lk')

#осуществление изменения информации профиля пользователя
class UserChangeInformation(Resource):
    def post(self):
        return {"result": insert_to_register(request.json, 'cng')}

    def get(self):
        return Response(render_template("changing.html"))

#осуществление скачивания истории запросов
class UserDownloadHistoryRequest(Resource):
    def post(self):
        return {"result": insert_to_register(request.json, 'downloadhisreq')}

#заполнение истории запросов
class UserMakeHistoryRequest(Resource):
    def post(self):
        return {"result": insert_to_register(request.json, 'makehisreq')}

#получение истории запросов для показа пользователю
class UserShowHistoryRequest(Resource):
    def post(self):
        return {"result": insert_to_register(request.json, 'showhisreq')}

#осуществление удаления истории запросов
class UserDeleteHistoryRequest(Resource):
    def post(self):
        return {"result": insert_to_register(request.json, 'delhisreq')}

#осуществление отправки ссобщения по футеру
class UserSendMessage(Resource):
    def post(self):
        return {"result": insert_to_register(request.json, 'sendmessage')}

#осуществление отправки кода подтверждения
class UserSendConfirm(Resource):
    def post(self):
        return {"result": insert_to_register(request.json, 'sendconfirm')}

#проверка кода подтверждения
class UserCheckConfirm(Resource):
    def post(self):
        return {"result": insert_to_register(request.json, 'checkconfirm')}

#случай удачного подтвеждения
class UserSuccessConfirm(Resource):
    def post(self):
        return {"result": insert_to_register(request.json, 'successconfirm')}

#осуществление подтверждения почты
class UserConfirmEmail(Resource):
    def get(self):
        return send_file("templates/emailConfirm.html")

#отправка файла с главной страницы
class MainPage(Resource):
    def get(self):
        return Response(render_template("index.html"))

#отправка файла с 1-ым способом поиска
class Sposob1(Resource):
    def get(self):
        return Response(render_template("sposob1.html"))

#отправка файла с 2-ым способом поиска
class Sposob2(Resource):
    def get(self):
        return Response(render_template("sposob2.html"))

#отправка файла с 3-им способом поиска
class Sposob3(Resource):
    def get(self):
        return Response(render_template("sposob3.html"))

#отправка файла с 4-ым способом поиска
class Sposob4(Resource):
    def get(self):
        return Response(render_template("sposob4.html"))

api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/enter')
api.add_resource(UserPasswordRecover, '/passwordrecover')
api.add_resource(UserLK, '/lk')
api.add_resource(UserInformation, '/info-lk')
api.add_resource(UserDownloadHistoryRequest, '/download-history-request')
api.add_resource(UserMakeHistoryRequest, '/make-history-request')
api.add_resource(UserShowHistoryRequest, '/show-history-request')
api.add_resource(UserDeleteHistoryRequest, '/delete-history-request')
api.add_resource(UserSendMessage, '/send-message')
api.add_resource(UserSendConfirm, '/send-confirm')
api.add_resource(UserCheckConfirm, '/check-confirm')
api.add_resource(UserSuccessConfirm, '/success-confirm')
api.add_resource(UserConfirmEmail, '/confirm')
api.add_resource(MainPage, '/')
api.add_resource(Sposob1, '/sp1')
api.add_resource(Sposob2, '/sp2')
api.add_resource(Sposob3, '/sp3')
api.add_resource(Sposob4, '/sp4')
api.add_resource(UserChangeInformation, '/changing')

if __name__ == '__main__':
    app.run(debug=True)
