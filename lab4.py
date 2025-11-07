from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)

    if x2 == 0:
        return render_template('lab4/div.html', error='Деление на ноль невозможно!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods=['POST'])
def sum_post():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')


@lab4.route('/lab4/mul', methods=['POST'])
def mul_post():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub_post():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/pow', methods=['POST'])
def pow_post():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='0⁰ не определено!')
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


tree_count = 0


@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Воробьев', 'gender': 'м'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Росс', 'gender': 'м'},
    {'login': 'tasya', 'password': '1205', 'name': 'Таисия Привалова', 'gender': 'ж'},
    {'login': 'vanya', 'password': '775', 'name': 'Иван Шевченко', 'gender': 'м'}
]


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login_name = session['name']
        else:
            authorized = False
            login_name = ''
        return render_template('lab4/login.html', authorized=authorized, login=login_name)

    login = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()

    if login == '':
        return render_template('lab4/login.html', error='Не введён логин', authorized=False, login=login)
    if password == '':
        return render_template('lab4/login.html', error='Не введён пароль', authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return redirect('/lab4/login')

    error = 'Неверный логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)



@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    temperature = None
    message = None
    error = None
    snowflakes = 0

    if request.method == 'POST':
        temp_str = request.form.get('temperature', '').strip()

        if temp_str == '':
            error = 'Ошибка: не задана температура.'
        else:
            try:
                temperature = float(temp_str)
                if temperature < -12:
                    error = 'Не удалось установить температуру — слишком низкое значение.'
                elif temperature > -1:
                    error = 'Не удалось установить температуру — слишком высокое значение.'
                elif -12 <= temperature <= -9:
                    message = f'Установлена температура: {temperature}°C'
                    snowflakes = 3
                elif -8 <= temperature <= -5:
                    message = f'Установлена температура: {temperature}°C'
                    snowflakes = 2
                elif -4 <= temperature <= -1:
                    message = f'Установлена температура: {temperature}°C'
                    snowflakes = 1
            except ValueError:
                error = 'Ошибка: температура должна быть числом.'

    return render_template('lab4/fridge.html',
                           temperature=temperature,
                           message=message,
                           error=error,
                           snowflakes=snowflakes)
