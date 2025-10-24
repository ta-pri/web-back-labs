from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name') or 'аноним'
    age = request.cookies.get('age') or 'неизвестен'
    name_color = request.cookies.get('name_color') or 'black'
    return render_template('lab3/lab3.html', name=name, age=age, name_color=name_color)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    errors1 = {}
    age = request.args.get('age')
    if age == '':
        errors1['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors, errors1=errors1)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    #Пусть кофе стоит 120 р, черный чай 80р, зеленый 70р
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    #Добавка молока удорожает на 30 р, а сахара на 10р
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')

    if color or bg_color or font_size or font_style:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_style:
            resp.set_cookie('font_style', font_style)
        return resp

    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_style = request.cookies.get('font_style')

    resp = make_response(render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, font_style=font_style))
    return resp


@lab3.route('/lab3/train')
def train_ticket():
    # Получаем данные из формы
    fio = request.args.get('fio')
    berth = request.args.get('berth')
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    age = request.args.get('age')
    from_city = request.args.get('from_city')
    to_city = request.args.get('to_city')
    date = request.args.get('date')
    insurance = request.args.get('insurance')

    errors = []

    # Если форма не отправлена — просто отрисовываем пустую
    if not fio and not from_city and not to_city:
        return render_template('lab3/train.html')

    # Проверка заполненности
    if not fio or not berth or not age or not from_city or not to_city or not date:
        errors.append("Все поля обязательны к заполнению.")
    else:
        # Проверка возраста
        try:
            age = int(age)
            if age < 1 or age > 120:
                errors.append("Возраст должен быть от 1 до 120 лет.")
        except ValueError:
            errors.append("Возраст должен быть числом.")

    # Если есть ошибки — показываем их
    if errors:
        return render_template('lab3/train.html', errors=errors,
                               fio=fio, berth=berth, linen=linen, luggage=luggage,
                               age=age, from_city=from_city, to_city=to_city, date=date,
                               insurance=insurance)

    # Расчёт стоимости
    price = 1000 if age >= 18 else 700
    if berth in ['нижняя', 'нижняя боковая']:
        price += 100
    if linen == 'on':
        price += 75
    if luggage == 'on':
        price += 250
    if insurance == 'on':
        price += 150

    ticket_type = "Детский билет" if age < 18 else "Взрослый билет"

    # Отображаем билет
    return render_template('lab3/ticket.html',
                           fio=fio, berth=berth, linen=linen,
                           luggage=luggage, age=age, from_city=from_city,
                           to_city=to_city, date=date, insurance=insurance,
                           price=price, ticket_type=ticket_type)


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_style')
    return resp


products = [
    {'name': 'iPhone 15', 'price': 120000, 'brand': 'Apple', 'color': 'черный'},
    {'name': 'Samsung Galaxy S24', 'price': 110000, 'brand': 'Samsung', 'color': 'серебристый'},
    {'name': 'Xiaomi 14', 'price': 85000, 'brand': 'Xiaomi', 'color': 'белый'},
    {'name': 'Google Pixel 8', 'price': 95000, 'brand': 'Google', 'color': 'черный'},
    {'name': 'Asus Zenfone 10', 'price': 78000, 'brand': 'Asus', 'color': 'синий'},
    {'name': 'Huawei P60 Pro', 'price': 89000, 'brand': 'Huawei', 'color': 'фиолетовый'},
    {'name': 'Nothing Phone 2', 'price': 70000, 'brand': 'Nothing', 'color': 'прозрачный'},
    {'name': 'Realme GT 5', 'price': 67000, 'brand': 'Realme', 'color': 'зеленый'},
    {'name': 'Honor Magic 6', 'price': 90000, 'brand': 'Honor', 'color': 'золотой'},
    {'name': 'OnePlus 12', 'price': 95000, 'brand': 'OnePlus', 'color': 'черный'},
    {'name': 'Sony Xperia 1 V', 'price': 112000, 'brand': 'Sony', 'color': 'фиолетовый'},
    {'name': 'Poco F6', 'price': 60000, 'brand': 'Poco', 'color': 'оранжевый'},
    {'name': 'Infinix GT 20', 'price': 45000, 'brand': 'Infinix', 'color': 'черный'},
    {'name': 'Tecno Phantom X3', 'price': 52000, 'brand': 'Tecno', 'color': 'голубой'},
    {'name': 'ZTE Nubia Z50', 'price': 64000, 'brand': 'ZTE', 'color': 'серый'},
    {'name': 'Motorola Edge 40', 'price': 68000, 'brand': 'Motorola', 'color': 'бежевый'},
    {'name': 'Vivo X100', 'price': 88000, 'brand': 'Vivo', 'color': 'синий'},
    {'name': 'Oppo Find X7', 'price': 97000, 'brand': 'Oppo', 'color': 'белый'},
    {'name': 'Meizu 21', 'price': 76000, 'brand': 'Meizu', 'color': 'серебристый'},
    {'name': 'Alcatel 3L', 'price': 32000, 'brand': 'Alcatel', 'color': 'черный'}
]


@lab3.route('/lab3/products')
def products_list():
    # минимальная и максимальная цены из списка
    min_price_all = min(p['price'] for p in products)
    max_price_all = max(p['price'] for p in products)

    # получаем значения из запроса или кук
    min_price = request.args.get('min_price') or request.cookies.get('min_price')
    max_price = request.args.get('max_price') or request.cookies.get('max_price')

    filtered = products

    # если пользователь нажал "Сброс"
    if request.args.get('reset'):
        resp = make_response(redirect('/lab3/products'))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp

    # если указаны оба значения — фильтруем
    if min_price or max_price:
        try:
            min_price = int(min_price) if min_price else min_price_all
            max_price = int(max_price) if max_price else max_price_all
            if min_price > max_price:
                min_price, max_price = max_price, min_price

            filtered = [p for p in products if min_price <= p['price'] <= max_price]

            resp = make_response(render_template(
                'lab3/products.html',
                products=filtered,
                min_price=min_price,
                max_price=max_price,
                min_price_all=min_price_all,
                max_price_all=max_price_all,
                count=len(filtered)
            ))
            resp.set_cookie('min_price', str(min_price))
            resp.set_cookie('max_price', str(max_price))
            return resp

        except ValueError:
            # если что-то не так — просто показать все
            filtered = products

    # если фильтра нет — показываем всё
    resp = make_response(render_template(
        'lab3/products.html',
        products=filtered,
        min_price=min_price,
        max_price=max_price,
        min_price_all=min_price_all,
        max_price_all=max_price_all,
        count=len(filtered)
    ))
    return resp