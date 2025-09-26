from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
           </body>
        </html>""", 200, {
            "X-Server": "sample",
            "Content-Type": "text/plain; charset=utf-8" 
        }

@app. route("/lab1/author")
def author():
    name = "Привалова Таисия Дмитриевна"
    group = "ФБИ-33"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """ </p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route('/lab1/image')
def image():
    path = url_for("static", filename="oak.jpg")
    css = url_for("static", filename="lab1.css")
    return f'''
<html>
    <head>
        <link rel="stylesheet" href="{css}">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="{path}">
    </body>
</html>
''', 200, {
    "Content-Type": "text/html; charset=utf-8",
    "Content-Language": "ru",            
    "X-My-Header-1": "Привет",          
    "X-My-Header-2": "12345"           
}

count = 0
@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
   <body>
      Сколько раз вы сюда заходили ''' + str(count) + '''
      <hr>
      Дата и время: ''' + str(time) + '''<br>
      Запрошенный адрес: ''' + url + '''<br>
      Ваш IP-адрес: ''' + client_ip + '''<br>
      <a href='/lab1/reset_counter'>Сбросить счётчик</a>
  </body>
</html>
'''

@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")


@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

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
      </ul>
      <hr>
      <footer>
         Привалова Таисия Дмитриевна, ФБИ-33, 3 курс, 2025 год
      </footer>
   </body>
</html>
"""

@app.route("/lab1")
def lab1():
    return """
<!doctype html>
<html>
   <head>
      <title>Лабораторная 1</title>
   </head>
   <body>
      Flask — фреймворк для создания веб-приложений на языке
      программирования Python, использующий набор инструментов
      Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
      называемых микрофреймворков — минималистичных каркасов веб-приложений, 
      сознательно предоставляющих лишь самые базовые возможности.
      <br><br>
      <a href='/'>На главную</a>
      <h2>Список роутов</h2>
      <ul>
         <li><a href='/lab1/web'>/lab1/web</a></li>
         <li><a href='/lab1/author'>/lab1/author</a></li>
         <li><a href='/lab1/image'>/lab1/image</a></li>
         <li><a href='/lab1/counter'>/lab1/counter</a></li>
         <li><a href='/lab1/reset_counter'>/lab1/reset_counter</a></li>
         <li><a href='/lab1/info'>/lab1/info</a></li>
         <li><a href='/lab1/created'>/lab1/created</a></li>
         <li><a href='/lab1/400'>/lab1/400</a></li>
         <li><a href='/lab1/401'>/lab1/401</a></li>
         <li><a href='/lab1/402'>/lab1/402</a></li>
         <li><a href='/lab1/403'>/lab1/403</a></li>
         <li><a href='/lab1/405'>/lab1/405</a></li>
         <li><a href='/lab1/418'>/lab1/418</a></li>
         <li><a href='/lab1/404'>/lab1/404</a></li>
         <li><a href='/lab1/error500'>/lab1/error500</a></li>
      </ul>
   </body>
</html>
"""

@app.route("/lab1/400")
def error_400():
    return "<h1>400 Bad Request</h1><p>Неверный запрос</p>", 400

@app.route("/lab1/401")
def error_401():
    return "<h1>401 Unauthorized</h1><p>Требуется авторизация</p>", 401

@app.route("/lab1/402")
def error_402():
    return "<h1>402 Payment Required</h1><p>Требуется оплата</p>", 402

@app.route("/lab1/403")
def error_403():
    return "<h1>403 Forbidden</h1><p>Доступ запрещён</p>", 403

@app.route("/lab1/405")
def error_405():
    return "<h1>405 Method Not Allowed</h1><p>Метод не разрешён</p>", 405

@app.route("/lab1/418")
def error_418():
    return "<h1>418 I'm a teapot</h1><p>Я чайник </p>", 418


log_404 = []  

@app.route("/lab1/404")
def page_404():
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



@app.route("/lab1/error500")
def error_500():
    x = 1 / 0
    return f"Результат: {x}" 

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
