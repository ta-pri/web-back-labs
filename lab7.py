from flask import Blueprint, render_template, request, abort, jsonify, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from datetime import datetime
lab7 = Blueprint('lab7', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='taisiia_privalova_knowledge_base',
            user='taisiia_privalova_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def validate_film(film):
    errors = {}
    
    if not film.get('title_ru'):
        errors['title_ru'] = 'Русское название не может быть пустым'
    
    if not film.get('title') and not film.get('title_ru'):
         errors['title'] = 'Укажите название'

    year = film.get('year')
    if not year:
         errors['year'] = 'Укажите год'
    else:
        try:
            year_int = int(year)
            current_year = datetime.now().year
            if year_int < 1895 or year_int > current_year:
                errors['year'] = f'Год должен быть от 1895 до {current_year}'
        except ValueError:
            errors['year'] = 'Некорректный год'

    description = film.get('description')
    if not description:
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    return errors

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films")
    rows = cur.fetchall()
    db_close(conn, cur)

    films_list = [dict(row) for row in rows]
    return jsonify(films_list)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?", (id,))
        
    row = cur.fetchone()
    db_close(conn, cur)
    
    if row is None:
        abort(404)
    return dict(row)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM films WHERE id = %s", (id,))
        row_count = cur.rowcount
    else:
        cur.execute("DELETE FROM films WHERE id = ?", (id,))
        row_count = cur.rowcount
        
    db_close(conn, cur)
    
    if row_count == 0:
        abort(404)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    
    errors = validate_film(film)
    if errors:
        return errors, 400

    if not film.get('title'):
        film['title'] = film['title_ru']

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM films WHERE id = %s", (id,))
    else:
        cur.execute("SELECT id FROM films WHERE id = ?", (id,))
        
    if cur.fetchone() is None:
        db_close(conn, cur)
        abort(404)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            UPDATE films 
            SET title=%s, title_ru=%s, year=%s, description=%s 
            WHERE id=%s
        """, (film['title'], film['title_ru'], film['year'], film['description'], id))
    else:
        cur.execute("""
            UPDATE films 
            SET title=?, title_ru=?, year=?, description=? 
            WHERE id=?
        """, (film['title'], film['title_ru'], film['year'], film['description'], id))
    
    db_close(conn, cur)
    return get_film(id)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    errors = validate_film(film)
    if errors:
        return errors, 400

    if not film.get('title'):
        film['title'] = film['title_ru']

    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description) 
            VALUES (%s, %s, %s, %s) RETURNING id
        """, (film['title'], film['title_ru'], film['year'], film['description']))
        new_id = cur.fetchone()['id']
    else:
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description) 
            VALUES (?, ?, ?, ?)
        """, (film['title'], film['title_ru'], film['year'], film['description']))
        new_id = cur.lastrowid
    
    db_close(conn, cur)
    
    return {"id": new_id}



