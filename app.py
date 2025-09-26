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

@app.route ('/lab1/image')
def image ():
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
    '''

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
      называемых микрофреймворков — минималистичных каркасов
      веб-приложений, сознательно предоставляющих лишь самые 
      базовые возможности.
      <br><br>
      <a href='/'>На главную</a>
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
