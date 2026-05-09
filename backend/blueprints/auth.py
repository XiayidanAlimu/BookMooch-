import sqlite3
import uuid
from flask import Blueprint, jsonify
from db import get_db
from utils import get_json_data, get_current_user, get_token_from_request

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = get_json_data()
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空。'}), 400

    db = get_db()
    user = db.execute(
        'SELECT id, username, fullname, email FROM users WHERE username = ? AND password = ?',
        (username, password),
    ).fetchone()
    if user is None:
        return jsonify({'error': '用户名或密码错误。'}), 401

    token = str(uuid.uuid4())
    db.execute('INSERT INTO sessions (token, user_id) VALUES (?, ?)', (token, user['id']))
    db.commit()

    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'fullname': user['fullname'],
            'email': user['email'],
        },
    })


@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = get_json_data()
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()
    fullname = (data.get('fullname') or '').strip()
    email = (data.get('email') or '').strip()

    if not username or not password or not fullname:
        return jsonify({'error': '用户名、密码和真实姓名不能为空。'}), 400

    db = get_db()
    try:
        cursor = db.execute(
            'INSERT INTO users (username, password, fullname, email) VALUES (?, ?, ?, ?)',
            (username, password, fullname, email),
        )
        db.commit()
        user_id = cursor.lastrowid
        user = db.execute('SELECT id, username, fullname, email FROM users WHERE id = ?', (user_id,)).fetchone()
        return jsonify(dict(user)), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': '用户名已存在。'}), 409


@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    token = get_token_from_request()
    if token:
        db = get_db()
        db.execute('DELETE FROM sessions WHERE token = ?', (token,))
        db.commit()
    return jsonify({'success': True})


@auth_bp.route('/api/me', methods=['GET'])
def me():
    user = get_current_user()
    if user is None:
        return jsonify({'error': '未登录。'}), 401

    db = get_db()
    count = db.execute('SELECT COUNT(*) AS total FROM books WHERE user_id = ?', (user['id'],)).fetchone()['total']
    user['donated_books_count'] = count
    return jsonify(user)
