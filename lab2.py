from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime


lab2 = Blueprint('lab2',__name__)


flower_list = [
    {"name": "роза", "price": 100},
    {"name": "тюльпан", "price": 70},
    {"name": "незабудка", "price": 50},
    {"name": "ромашка", "price": 40},
]


@lab2.route('/lab2/flowers/delete/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect('/lab2/all_flowers') 

    
@lab2.route('/lab2/add_flower/')
def add_flower_no_name():
    return "вы не задали имя цветка", 400


@lab2.route('/lab2/example')
def example():
  name, lab, grup, curs = 'Таисия Привалова', 2, 'ФБИ-33', 3
  fruits = [
      {'name': 'яблоки', 'price': 100},
      {'name': 'груши', 'price': 120},
      {'name': 'апельсины', 'price': 80},
      {'name': 'мандарины', 'price': 95},
      {'name': 'манго', 'price': 321}
  ]
  return render_template('lab2/example.html',
                         name=name, lab=lab, grup=grup,
                         curs=curs, fruits=fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)


@lab2.route('/lab2/add_flower/', methods=['POST'])
def add_flower_post():
    name = request.form.get("name")
    price = request.form.get("price")
    if not name or not price:
        return "Ошибка: не заданы имя или цена", 400
    flower_list.append({"name": name, "price": int(price)})
    return redirect("/lab2/all_flowers")


@lab2.route('/lab2/all_flowers')
def all_flowers():
    return render_template("lab2/flowers.html", flowers=flower_list)


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/all_flowers')


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calc_one(a):
    return redirect(f'/lab2/calc/{a}/1')


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('lab2/calc.html', a=a, b=b)


@lab2.route('/lab2/books')
def books():
    books = [
        {'title': 'Мастер и Маргарита', 'author': 'М. Булгаков', 'genre': 'Роман', 'pages': 480},
        {'title': 'Преступление и наказание', 'author': 'Ф. Достоевский', 'genre': 'Роман', 'pages': 600},
        {'title': 'Евгений Онегин', 'author': 'А. Пушкин', 'genre': 'Поэма', 'pages': 250},
        {'title': 'Гарри Поттер', 'author': 'Дж. Роулинг', 'genre': 'Фэнтези', 'pages': 430},
        {'title': '1984', 'author': 'Дж. Оруэлл', 'genre': 'Антиутопия', 'pages': 320},
        {'title': 'Война и мир', 'author': 'Л. Толстой', 'genre': 'Роман', 'pages': 1300},
        {'title': 'Алиса в Стране чудес', 'author': 'Л. Кэрролл', 'genre': 'Сказка', 'pages': 200},
        {'title': 'Три товарища', 'author': 'Э. М. Ремарк', 'genre': 'Роман', 'pages': 480},
        {'title': 'Шерлок Холмс', 'author': 'А. Конан Дойль', 'genre': 'Детектив', 'pages': 520},
        {'title': 'Маленький принц', 'author': 'А. де Сент-Экзюпери', 'genre': 'Притча', 'pages': 120},
    ]
    return render_template('lab2/books.html', books=books)


@lab2.route('/lab2/fruits')
def fruits():
    fruits = [
        {'name': 'Яблоко', 'desc': 'Сладкий и сочный фрукт, символ здоровья.', 'img': 'lab2/apple.jpg'},
        {'name': 'Банан', 'desc': 'Мягкий и питательный фрукт с высоким содержанием калия.', 'img': 'lab2/banana.jpg'},
        {'name': 'Апельсин', 'desc': 'Цитрус с ярким вкусом и высоким содержанием витамина C.', 'img': 'lab2/orange.jpg'},
        {'name': 'Груша', 'desc': 'Ароматный и нежный фрукт, богат клетчаткой.', 'img': 'lab2/pear.jpg'},
        {'name': 'Ананас', 'desc': 'Тропический фрукт с освежающей кислинкой.', 'img': 'lab2/pineapple.jpg'},
        {'name': 'Киви', 'desc': 'Фрукт с зелёной мякотью и множеством витаминов.', 'img': 'lab2/kiwi.jpg'},
        {'name': 'Клубника', 'desc': 'Сочная и сладкая ягода, любимая летом.', 'img': 'lab2/strawberry.jpg'},
        {'name': 'Вишня', 'desc': 'Кисло-сладкая ягода, из которой делают варенье.', 'img': 'lab2/cherry.jpg'},
        {'name': 'Слива', 'desc': 'Фиолетовый плод с нежной мякотью.', 'img': 'lab2/plum.jpg'},
        {'name': 'Малина', 'desc': 'Ароматная ягода, богатая витаминами.', 'img': 'lab2/raspberry.jpg'},
        {'name': 'Черника', 'desc': 'Полезная лесная ягода для зрения.', 'img': 'lab2/blueberry.jpg'},
        {'name': 'Манго', 'desc': 'Сладкий фрукт с тропическим ароматом.', 'img': 'lab2/mango.jpg'},
        {'name': 'Арбуз', 'desc': 'Летняя ягода с сочной красной мякотью.', 'img': 'lab2/watermelon.jpg'},
        {'name': 'Дыня', 'desc': 'Сладкий ароматный плод, похож на мед.', 'img': 'lab2/melon.jpg'},
        {'name': 'Гранат', 'desc': 'Фрукт с множеством рубиновых зёрен.', 'img': 'lab2/pomegranate.jpg'},
        {'name': 'Лимон', 'desc': 'Кислый цитрус, источник витамина C.', 'img': 'lab2/lemon.jpg'},
        {'name': 'Персик', 'desc': 'Мягкий бархатный фрукт с косточкой.', 'img': 'lab2/peach.jpg'},
        {'name': 'Абрикос', 'desc': 'Оранжевый фрукт с нежным вкусом.', 'img': 'lab2/apricot.jpg'},
        {'name': 'Кокос', 'desc': 'Тропический плод с белой мякотью и соком.', 'img': 'lab2/coconut.jpg'},
        {'name': 'Грейпфрут', 'desc': 'Крупный цитрус с горьковатым вкусом.', 'img': 'lab2/grapefruit.jpg'}
    ]
    return render_template('lab2/fruits.html', fruits=fruits)
