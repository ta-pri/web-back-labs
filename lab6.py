from flask import Blueprint, render_template, request, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)


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


@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    req_id = data.get('id')
    method = data.get('method')

    if method == 'info':
        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")
        else:
            cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")

        rows = cur.fetchall()
        offices = [dict(row) for row in rows]

        db_close(conn, cur)

        return {
            "jsonrpc": "2.0",
            "result": offices,
            "id": req_id
        }


    login = session.get('login')
    if not login:
        return {
            "jsonrpc": "2.0",
            "error": {"code": 1, "message": "Unauthorized"},
            "id": req_id
        }

    if method == 'booking':
        office_number = data['params']

        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number=%s;", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number=?;", (office_number,))
        office = cur.fetchone()

        if office is None:
            db_close(conn, cur)
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32602, "message": "Invalid params"},
                "id": req_id
            }

        if office['tenant'] != "":
            db_close(conn, cur)
            return {
                "jsonrpc": "2.0",
                "error": {"code": 2, "message": "Office already booked"},
                "id": req_id
            }

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE offices SET tenant=%s WHERE number=%s;", (login, office_number))
        else:
            cur.execute("UPDATE offices SET tenant=? WHERE number=?;", (login, office_number))

        db_close(conn, cur)

        return {"jsonrpc": "2.0", "result": "success", "id": req_id}

    if method == 'cancellation':
        office_number = data['params']

        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number=%s;", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number=?;", (office_number,))
        office = cur.fetchone()

        if office is None:
            db_close(conn, cur)
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32602, "message": "Invalid params"},
                "id": req_id
            }

        if office['tenant'] == "":
            db_close(conn, cur)
            return {
                "jsonrpc": "2.0",
                "error": {"code": 3, "message": "Office not booked"},
                "id": req_id
            }

        if office['tenant'] != login:
            db_close(conn, cur)
            return {
                "jsonrpc": "2.0",
                "error": {"code": 4, "message": "Forbidden"},
                "id": req_id
            }

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE offices SET tenant='' WHERE number=%s;", (office_number,))
        else:
            cur.execute("UPDATE offices SET tenant='' WHERE number=?;", (office_number,))

        db_close(conn, cur)

        return {"jsonrpc": "2.0", "result": "success", "id": req_id}

    return {
        "jsonrpc": "2.0",
        "error": {"code": -32601, "message": "Method not found"},
        "id": req_id
    }
