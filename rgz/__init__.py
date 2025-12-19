from flask import Blueprint, render_template, request, abort, jsonify, current_app, session, redirect, url_for
import sqlite3
from os import path
import os
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import random

rgz = Blueprint('rgz', __name__, template_folder='templates', static_folder='static')

db_path = path.join(path.dirname(path.realpath(__file__)), "rgz.db")
UPLOAD_FOLDER = path.join(path.dirname(path.dirname(path.realpath(__file__))), 'static', 'rgz', 'uploads')

def db_connect():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.create_function("lower", 1, lambda s: s.lower() if s else s)
    cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@rgz.route('/rgz/')
def index():
    return render_template('rgz/index.html')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        conn, cur = db_connect()
        cur.execute("SELECT * FROM users WHERE login = ?", (login,))
        user = cur.fetchone()
        db_close(conn, cur)

        if user and check_password_hash(user['password'], password):
            session['rgz_admin'] = True
            return redirect(url_for('rgz.admin_dashboard'))
        else:
            return render_template('rgz/login.html', error="Неверный логин или пароль")
    
    return render_template('rgz/login.html')

@rgz.route('/rgz/logout')
def logout():
    session.pop('rgz_admin', None)
    return redirect(url_for('rgz.index'))

@rgz.route('/rgz/admin')
def admin_dashboard():
    if not session.get('rgz_admin'):
        return redirect(url_for('rgz.login'))
    
    search_title = request.args.get('title', '')
    search_author = request.args.get('author', '')
    
    conn, cur = db_connect()
    
    query = "SELECT * FROM books WHERE 1=1"
    params = []
    
    if search_title:
        query += " AND lower(title) LIKE lower(?)"
        params.append(f"%{search_title}%")
    
    if search_author:
        query += " AND lower(author) LIKE lower(?)"
        params.append(f"%{search_author}%")
    
    query += " ORDER BY id DESC"
    
    cur.execute(query, tuple(params))
    books = [dict(row) for row in cur.fetchall()]
    db_close(conn, cur)
    
    return render_template('rgz/admin.html', 
                           books=books, 
                           search_title=search_title, 
                           search_author=search_author)

@rgz.route('/rgz/admin/add', methods=['POST'])
def add_book():
    if not session.get('rgz_admin'):
        abort(403)

    title = request.form.get('title')
    author = request.form.get('author')
    pages = request.form.get('pages')
    publisher = request.form.get('publisher')
    file = request.files.get('cover')
    
    cover_url = "/static/rgz/book_placeholder.jpg"

    if file and file.filename != '':
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_filename = f"{timestamp}_{filename}"
        
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
            
        file.save(os.path.join(UPLOAD_FOLDER, new_filename))
        cover_url = url_for('static', filename=f'rgz/uploads/{new_filename}')

    conn, cur = db_connect()
    cur.execute("""
        INSERT INTO books (title, author, pages, publisher, cover_url)
        VALUES (?, ?, ?, ?, ?)
    """, (title, author, pages, publisher, cover_url))
    db_close(conn, cur)

    return redirect(url_for('rgz.admin_dashboard'))

@rgz.route('/rgz/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    if not session.get('rgz_admin'):
        return redirect(url_for('rgz.login'))

    conn, cur = db_connect()

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        pages = request.form.get('pages')
        publisher = request.form.get('publisher')
        file = request.files.get('cover')

        cur.execute("SELECT cover_url FROM books WHERE id = ?", (id,))
        current_cover = cur.fetchone()['cover_url']
        new_cover_url = current_cover

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_filename = f"{timestamp}_{filename}"
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file.save(os.path.join(UPLOAD_FOLDER, new_filename))
            new_cover_url = url_for('static', filename=f'rgz/uploads/{new_filename}')

        cur.execute("""
            UPDATE books 
            SET title = ?, author = ?, pages = ?, publisher = ?, cover_url = ?
            WHERE id = ?
        """, (title, author, pages, publisher, new_cover_url, id))
        
        db_close(conn, cur)
        return redirect(url_for('rgz.admin_dashboard'))

    cur.execute("SELECT * FROM books WHERE id = ?", (id,))
    book = cur.fetchone()
    db_close(conn, cur)

    if not book:
        abort(404)

    return render_template('rgz/edit.html', book=dict(book))

@rgz.route('/rgz/admin/delete/<int:id>', methods=['POST'])
def delete_book_post(id):
    if not session.get('rgz_admin'):
        abort(403)
    
    conn, cur = db_connect()
    cur.execute("DELETE FROM books WHERE id = ?", (id,))
    db_close(conn, cur)
    return redirect(url_for('rgz.admin_dashboard'))

@rgz.route('/rgz/api/books', methods=['GET'])
def get_books():
    conn, cur = db_connect()
    page = request.args.get('page', 1, type=int)
    limit = 20
    offset = (page - 1) * limit
    
    author = request.args.get('author')
    title = request.args.get('title')
    publisher = request.args.get('publisher')
    min_pages = request.args.get('min_pages')
    max_pages = request.args.get('max_pages')
    sort_by = request.args.get('sort_by', 'title')

    query = "SELECT * FROM books WHERE 1=1"
    params = []
    
    if author:
        query += " AND lower(author) LIKE lower(?)"
        params.append(f"%{author}%")
    if title:
        query += " AND lower(title) LIKE lower(?)"
        params.append(f"%{title}%")
    if publisher:
        query += " AND lower(publisher) LIKE lower(?)"
        params.append(f"%{publisher}%")
        
    if min_pages:
        query += " AND pages >= ?"
        params.append(min_pages)
    if max_pages:
        query += " AND pages <= ?"
        params.append(max_pages)

    allowed_sort = ['title', 'author', 'pages', 'publisher']
    if sort_by not in allowed_sort:
        sort_by = 'title'
    
    count_query = query.replace("SELECT *", "SELECT COUNT(*) as cnt")
    cur.execute(count_query, tuple(params))
    total_books = cur.fetchone()['cnt']

    query += f" ORDER BY {sort_by} LIMIT {limit} OFFSET {offset}"
    cur.execute(query, tuple(params))
    
    books = [dict(row) for row in cur.fetchall()]
    db_close(conn, cur)
    
    return jsonify({
        'books': books,
        'total': total_books,
        'page': page,
        'pages_total': (total_books + limit - 1) // limit if total_books > 0 else 1
    })

@rgz.route('/rgz/init')
def init_db():
    conn, cur = db_connect()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            pages INTEGER NOT NULL,
            publisher TEXT NOT NULL,
            cover_url TEXT
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            login TEXT UNIQUE NOT NULL, 
            password TEXT NOT NULL
        );
    """)
    
    cur.execute("SELECT id FROM users WHERE login = 'admin'")
    if not cur.fetchone():
        password_hash = generate_password_hash('123')
        cur.execute("INSERT INTO users (login, password) VALUES ('admin', ?)", (password_hash,))

    cur.execute("DELETE FROM books") 
    cur.execute("DELETE FROM sqlite_sequence WHERE name='books'") 

    real_books = [
        {"title": "Мастер и Маргарита", "author": "М. Булгаков", "pages": 480, "publisher": "Азбука"},
        {"title": "Преступление и наказание", "author": "Ф. Достоевский", "pages": 672, "publisher": "Эксмо"},
        {"title": "Война и мир", "author": "Л. Толстой", "pages": 1274, "publisher": "АСТ"},
        {"title": "Анна Каренина", "author": "Л. Толстой", "pages": 864, "publisher": "Азбука"},
        {"title": "Евгений Онегин", "author": "А. Пушкин", "pages": 192, "publisher": "Детская литература"},
        {"title": "Герой нашего времени", "author": "М. Лермонтов", "pages": 224, "publisher": "Эксмо"},
        {"title": "Мертвые души", "author": "Н. Гоголь", "pages": 352, "publisher": "АСТ"},
        {"title": "Собачье сердце", "author": "М. Булгаков", "pages": 160, "publisher": "Азбука"},
        {"title": "Отцы и дети", "author": "И. Тургенев", "pages": 288, "publisher": "Росмэн"},
        {"title": "Вишневый сад", "author": "А. Чехов", "pages": 96, "publisher": "Детская литература"},
        {"title": "Братья Карамазовы", "author": "Ф. Достоевский", "pages": 992, "publisher": "Эксмо"},
        {"title": "Идиот", "author": "Ф. Достоевский", "pages": 640, "publisher": "АСТ"},
        {"title": "Двенадцать стульев", "author": "И. Ильф, Е. Петров", "pages": 416, "publisher": "Азбука"},
        {"title": "Золотой теленок", "author": "И. Ильф, Е. Петров", "pages": 384, "publisher": "Росмэн"},
        {"title": "Пикник на обочине", "author": "Братья Стругацкие", "pages": 256, "publisher": "АСТ"},
        {"title": "Трудно быть богом", "author": "Братья Стругацкие", "pages": 224, "publisher": "Азбука"},
        {"title": "Алиса в Стране чудес", "author": "Л. Кэрролл", "pages": 180, "publisher": "Махаон"},
        {"title": "Гарри Поттер и философский камень", "author": "Дж. Роулинг", "pages": 432, "publisher": "Махаон"},
        {"title": "1984", "author": "Дж. Оруэлл", "pages": 320, "publisher": "АСТ"},
        {"title": "Унесенные ветром", "author": "М. Митчелл", "pages": 1024, "publisher": "Эксмо"}
    ]

    editions = ["(Мягкая обложка)", "(Твердая обложка)", "(Подарочное издание)"]
    count_real = 0
    for edition in editions:
        for b in real_books:
            full_title = f"{b['title']} {edition}"
            cur.execute("""
                INSERT INTO books (title, author, pages, publisher, cover_url) 
                VALUES (?, ?, ?, ?, ?)
            """, (full_title, b['author'], b['pages'], b['publisher'], "/static/rgz/book_placeholder.jpg"))
            count_real += 1

    target_count = 100
    count_random = 0
    gen_authors = ["Стивен Кинг", "Нил Гейман", "Дж. Р. Р. Толкин", "Агата Кристи", "Рэй Брэдбери", "Харуки Мураками", "Дэн Браун"]
    gen_publishers = ["АСТ", "Эксмо", "Азбука", "Росмэн", "Альпина"]
    titles_adjectives = ["Темная", "Загадочная", "Последняя", "Вечная", "Смертельная", "Невероятная", "Тихая", "Громкая"]
    titles_nouns = ["Башня", "История", "Игра", "Зима", "Ночь", "Империя", "Звезда", "Дорога", "Тайна"]
    
    while (count_real + count_random) < target_count:
        t = f"{random.choice(titles_adjectives)} {random.choice(titles_nouns)}"
        a = random.choice(gen_authors)
        p = random.randint(150, 850)
        pub = random.choice(gen_publishers)
        cur.execute("""
            INSERT INTO books (title, author, pages, publisher, cover_url) 
            VALUES (?, ?, ?, ?, ?)
        """, (t, a, p, pub, "/static/rgz/book_placeholder.jpg"))
        count_random += 1

    db_close(conn, cur)
    return f"Готово! База очищена. Добавлено: {count_real} реальных вариантов + {count_random} случайных книг. Всего: {count_real + count_random}."