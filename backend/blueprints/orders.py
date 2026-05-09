import sqlite3
from flask import Blueprint, jsonify
from db import get_db
from utils import get_json_data, get_current_user

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/api/books/<int:book_id>/wishlist', methods=['POST'])
def add_to_wishlist(book_id):
    user = get_current_user()
    if user is None:
        return jsonify({'error': '请先登录后添加心愿单。'}), 401

    db = get_db()
    book = db.execute('SELECT id FROM books WHERE id = ?', (book_id,)).fetchone()
    if book is None:
        return jsonify({'error': '图书不存在。'}), 404

    try:
        db.execute('INSERT INTO wishlist (user_id, book_id) VALUES (?, ?)', (user['id'], book_id))
        db.commit()
        return jsonify({'success': True, 'message': '图书已加入心愿单。'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': '该图书已在心愿单中。'}), 409


@orders_bp.route('/api/books/<int:book_id>/wishlist', methods=['DELETE'])
def remove_from_wishlist(book_id):
    user = get_current_user()
    if user is None:
        return jsonify({'error': '请先登录后操作心愿单。'}), 401

    db = get_db()
    db.execute('DELETE FROM wishlist WHERE user_id = ? AND book_id = ?', (user['id'], book_id))
    db.commit()
    return jsonify({'success': True})


@orders_bp.route('/api/wishlist', methods=['GET'])
def get_wishlist():
    user = get_current_user()
    if user is None:
        return jsonify({'error': '请先登录后查看心愿单。'}), 401

    db = get_db()
    rows = db.execute(
        '''SELECT w.id, b.id AS book_id, b.title, b.author, b.isbn, b.cover_url, b.description,
                  c.name AS category_name, u.fullname AS donor, w.created_at
           FROM wishlist w
           JOIN books b ON w.book_id = b.id
           LEFT JOIN categories c ON b.category_id = c.id
           LEFT JOIN users u ON b.user_id = u.id
           WHERE w.user_id = ?
           ORDER BY w.created_at DESC''',
        (user['id'],),
    ).fetchall()
    return jsonify([dict(row) for row in rows])


@orders_bp.route('/api/books/<int:book_id>/order', methods=['POST'])
def place_order(book_id):
    user = get_current_user()
    if user is None:
        return jsonify({'error': '请先登录后下单。'}), 401

    data = get_json_data()
    recipient_name = (data.get('recipient_name') or '').strip()
    address = (data.get('address') or '').strip()
    phone = (data.get('phone') or '').strip()
    note = (data.get('note') or '').strip()

    if not recipient_name or not address:
        return jsonify({'error': '收件人姓名和邮寄地址不能为空。'}), 400

    db = get_db()
    book = db.execute('SELECT id, user_id FROM books WHERE id = ?', (book_id,)).fetchone()
    if book is None:
        return jsonify({'error': '图书不存在。'}), 404
    if book['user_id'] == user['id']:
        return jsonify({'error': '不能领取自己的捐赠图书。'}), 400

    cursor = db.execute(
        'INSERT INTO orders (user_id, book_id, recipient_name, address, phone, note) VALUES (?, ?, ?, ?, ?, ?)',
        (user['id'], book_id, recipient_name, address, phone, note),
    )
    db.commit()

    order_id = cursor.lastrowid
    order = db.execute(
        '''SELECT o.id, o.recipient_name, o.address, o.phone, o.note, o.status, o.created_at,
                  b.id AS book_id, b.title, b.author, b.cover_url, u.fullname AS donor
           FROM orders o
           JOIN books b ON o.book_id = b.id
           LEFT JOIN users u ON b.user_id = u.id
           WHERE o.id = ?''',
        (order_id,),
    ).fetchone()
    return jsonify(dict(order)), 201


@orders_bp.route('/api/orders', methods=['GET'])
def get_orders():
    user = get_current_user()
    if user is None:
        return jsonify({'error': '请先登录后查看订单。'}), 401

    db = get_db()
    rows = db.execute(
        '''SELECT o.id, o.recipient_name, o.address, o.phone, o.note, o.status, o.created_at,
                  b.id AS book_id, b.title, b.author, b.cover_url, u.fullname AS donor
           FROM orders o
           JOIN books b ON o.book_id = b.id
           LEFT JOIN users u ON b.user_id = u.id
           WHERE o.user_id = ?
           ORDER BY o.created_at DESC''',
        (user['id'],),
    ).fetchall()
    return jsonify([dict(row) for row in rows])
