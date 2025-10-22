from flask import Flask, url_for, request, redirect, abort, render_template
from lab1 import lab1
from lab2 import lab2
import datetime


app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)


log_404 = []


@app.errorhandler(404)
def not_found(err):
    css = url_for("static", filename="lab1.css")
    img_path = url_for("static", filename="404.jpg")
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

