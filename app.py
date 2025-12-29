from flask import Flask, url_for, request, redirect, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from db import db
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

from rgz import rgz

import datetime
import os
from os import path

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'sqlite')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'taisiia_privalova_orm'
    db_user = 'taisiia_privalova_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
  dir_path = path.dirname(path.realpath(__file__))
  db_path = path.join(dir_path, "taisiia_privalova_orm.db")
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)

app.register_blueprint(rgz)

log_404 = []


@app.errorhandler(404)
def not_found(err):
    css = url_for("static", filename="lab1/lab1.css")
    img_path = url_for("static", filename="lab1/404.jpg")
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    log_404.append(f"[{access_time}, пользователь {client_ip}] зашёл на адрес: {url}")
    log_html = "<ul>"
    for entry in log_404:
        log_html += f"<li>{entry}</li>"
    log_html += "</ul>"
    return f'''
    <html>
        <head>
            <link rel="stylesheet" href="{css}">
        </head>
        <body>
            <h1>404 — Ой! Что-то пошло не так</h1>
            <p>Страница, которую вы ищете, не найдена.</p>
            <img src="{img_path}" alt="404">
            <p>Ваш IP: {client_ip}</p>
            <p>Дата и время доступа: {access_time}</p>
            <a href='/'>На главную</a>
            <hr>
            <h3>Журнал посещений 404:</h3>
            {log_html}
        </body>
    </html>
    ''', 404 


@app.route("/")
@app.route("/index")
def index():
    return """
<!doctype html>
<html>
   <head>
      <title>НГТУ, ФБ, Лабораторные работы</title>
   </head>
   <body>
      <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
      <ul>
         <li><a href='/lab1'>Первая лабораторная</a></li>
         <li><a href="/lab2">Вторая лабораторная</a></li>
         <li><a href="/lab3">Третья лабораторная</a></li>
         <li><a href="/lab4">Четвертая лабораторная</a></li>
         <li><a href="/lab5">Пятая лабораторная</a></li>
         <li><a href="/lab6">Шестая лабораторная</a></li>
         <li><a href="/lab7">Седьмая лабораторная</a></li>
         <li><a href="/lab8">Восьмая лабораторная</a></li>
         <li><a href="/rgz/">РГЗ (Книги)</a></li>
      </ul>
      <hr>
      <footer>
         Привалова Таисия Дмитриевна, ФБИ-33, 3 курс, 2025 год
      </footer>
   </body>
</html>
""" 


@app.errorhandler(500)
def internal_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка сервера</title>
        <style>
            h1 { color: #ff4d4d; }
            p { font-size: 18px; }
        </style>
    </head>
    <body>
        <h1>500 — Внутренняя ошибка сервера</h1>
        <p>Произошла ошибка на сервере. Попробуйте позже.</p>
    </body>
</html>
''', 500

