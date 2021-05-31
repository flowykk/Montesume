from flask import Flask
from flask import request, redirect, url_for, send_file
from pymysql.cursors import DictCursor
from contextlib import closing
from hashlib import sha256
from flask import render_template
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required #, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
import pymysql

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]
app.config['JWT_BLACKLIST_ENABLED'] = True
jwt = JWTManager(app)
app.config['PROPAGATE_EXCEPTIONS'] = True

def insert_to_register(message, mode):
    with closing(pymysql.connect(host="localhost", user="b92599ho_ivr", password="gQz6g3H*", db="b92599ho_ivr", charset="utf8", use_unicode=True, cursorclass=DictCursor)) as connection:
        with connection.cursor() as cursor:
            if mode == 'reg':
                user_table = cursor.execute("select * from users where email=%s", message['email'])
                if user_table == 0:
                    if check_password(message['password']):
                        token = Hash(message['email'] + message['password'])
                        query = "INSERT INTO `users` (`id`, `name`,`email`, `token`) VALUES (NULL,'"+message['name']+"', '"+message['email']+"', '"+token+"')"
                        cursor.execute(query)
                        connection.commit()
                        access_token = create_access_token(identity=token)
                        refresh_token = create_refresh_token(identity=token)

                        f = "SELECT `id` FROM `users` WHERE `token`='{}'".format(token)
                        cursor.execute(f)
                        id_find = cursor.fetchall()

                        query ="INSERT INTO `JWT` (`user_id`, `access_token`) VALUES ( '" + str(id_find[0]['id']) + "', '" + access_token + "')"
                        cursor.execute(query)
                        connection.commit()

                        return {"access_token": access_token, "refresh_token": refresh_token}
                    else: return False
                else:
                    return False
            elif mode == 'ent':
                token = Hash(message['email'] + message['password'])
                user_table = cursor.execute("select * from users where token=%s", token)
                if user_table != 0:
                    access_token = create_access_token(identity=token)
                    refresh_token = create_refresh_token(identity=token)

                    f = "SELECT `id` FROM `users` WHERE `token`='{}'".format(token)
                    cursor.execute(f)
                    id_find = cursor.fetchall()

                    query = "INSERT INTO `JWT` (`user_id`, `access_token`) VALUES ( '" + str(id_find[0]['id']) + "', '" + access_token + "')"
                    cursor.execute(query)
                    connection.commit()

                    return {"access_token": access_token, "refresh_token": refresh_token}
                else:
                    return False
            else:
                f = "SELECT `user_id` FROM `JWT` WHERE `access_token`='{}'".format(message)
                cursor.execute(f)
                id_find = cursor.fetchall()
                id = (str(id_find[0]['user_id']))
                string = "SELECT `email`, `name` FROM `users` WHERE `id`='{}'".format(id)
                cursor.execute(string)
                fullstring = cursor.fetchall()
                return fullstring[0]



def Hash(input):
    return sha256(input.encode('utf-8')).hexdigest()
    
@app.route('/register', methods= ['GET', 'POST'])
def register():
    if request.method == "POST":
        result = insert_to_register(request.json, 'reg')
        if result == False:
            return '''Вы ввели невалидный пароль или пользователь с таким email уже существует'''
        else:
            return result["access_token"]
    else:
        return render_template("register.html")
    
@app.route('/enter', methods= ['GET', 'POST'])
def enter():
    if request.method == "POST":
        result = insert_to_register(request.json, 'ent')
        if result == False:
            return '''Такого пользователя не существует'''
        else:
            return result["access_token"]
    else:
        return render_template("enter.html")
        
@app.route('/sp1', methods= ['GET', 'POST'])
def sp1():
    return render_template("sposob1.html")
    
@app.route('/sp2', methods= ['GET', 'POST'])
def sp2():
    return render_template("sposob2.html")
    
@app.route('/sp3', methods= ['GET', 'POST'])
def sp3():
    return render_template("sposob3.html")
    
@app.route('/sp4', methods= ['GET', 'POST'])
def sp4():
    return render_template("sposob4.html")
    
@app.route('/', methods= ['GET', 'POST'])
def route():
    return render_template("index.html")
    
@app.route('/lk', methods= ['GET', 'POST'])
@jwt_required()
def lk():
    return send_file("templates/pr_office.html")


@app.route('/info-lk', methods= ['GET', 'POST'])
def info_lk():
    if request.method == "GET":
        result = insert_to_register(request.headers['Authorization'][7:], 'info-lk')
        return result


def check_password(password):
    if len(password) < 6: return False
    else: return True


if __name__=='__main__':
    app.run(debug=True)
