import requests
from flask import Blueprint, jsonify, request
from db import get_db
from utils import get_json_data, get_current_user

books_bp = Blueprint('books', __name__)


@books_bp.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        db = get_db()
        rows = db.execute('SELECT id, name FROM categories ORDER BY id').fetchall()
        return jsonify([dict(row) for row in rows])
    except Exception as e:
        books_bp.logger.error('Error in /api/categories', exc_info=True)
        return jsonify({'error': str(e)}), 500


@books_bp.route('/api/book-search', methods=['GET'])
def book_search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])

    try:
        response = requests.get(
            'https://openlibrary.org/search.json',
            params={'q': query, 'limit': 12},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        results = []
        for idx, doc in enumerate(data.get('docs', [])):
            title = doc.get('title') or ''
            author = (doc.get('author_name') or [''])[0]
            isbn_list = doc.get('isbn') or []
            isbn = isbn_list[0] if isbn_list else ''
            cover_id = doc.get('cover_i')
            cover_url = None
            if cover_id:
                cover_url = f'https://covers.openlibrary.org/b/id/{cover_id}-M.jpg'
            elif isbn:
                cover_url = f'https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg'

            results.append({
                'id': doc.get('key', f'openlib-{idx}'),
                'title': title,
                'author': author,
                'isbn': isbn,
                'cover_url': cover_url,
            })
        return jsonify(results)
    except Exception as e:
        books_bp.logger.error('Error in /api/book-search', exc_info=True)
        return jsonify({'error': '图书搜索接口失败，请稍后重试。'}), 500


@books_bp.route('/api/books', methods=['GET'])
def get_books():
    db = get_db()
    category_id = request.args.get('category_id')
    query = '''SELECT b.id, b.title, b.author, b.isbn, b.cover_url, b.description, b.donated_at,
                      c.name AS category_name, u.fullname AS donor
               FROM books b
               LEFT JOIN categories c ON b.category_id = c.id
               LEFT JOIN users u ON b.user_id = u.id'''
    params = []
    if category_id:
        query += ' WHERE b.category_id = ?'
        params.append(category_id)
    query += ' ORDER BY b.donated_at DESC'

    rows = db.execute(query, params).fetchall()
    books = [dict(row) for row in rows]
    return jsonify(books)


@books_bp.route('/api/books', methods=['POST'])
def add_book():
    user = get_current_user()
    if user is None:
        return jsonify({'error': '请先登录后提交捐书。'}), 401

    data = get_json_data()
    title = (data.get('title') or '').strip()
    author = (data.get('author') or '').strip()
    isbn = (data.get('isbn') or '').strip()
    description = (data.get('description') or '').strip()
    category_id = data.get('category_id')
    cover_url = (data.get('cover_url') or '').strip()

    if not title or not author:
        return jsonify({'error': '标题和作者为必填字段。'}), 400

    db = get_db()
    if category_id:
        category = db.execute('SELECT id FROM categories WHERE id = ?', (category_id,)).fetchone()
        if category is None:
            return jsonify({'error': '所选分类不存在。'}), 400

    cursor = db.execute(
        'INSERT INTO books (title, author, isbn, cover_url, description, category_id, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (title, author, isbn, cover_url, description, category_id, user['id']),
    )
    db.commit()

    book_id = cursor.lastrowid
    book = db.execute(
        '''SELECT b.id, b.title, b.author, b.isbn, b.cover_url, b.description, b.donated_at,
                  c.name AS category_name, u.fullname AS donor
           FROM books b
           LEFT JOIN categories c ON b.category_id = c.id
           LEFT JOIN users u ON b.user_id = u.id
           WHERE b.id = ?''',
        (book_id,),
    ).fetchone()
    return jsonify(dict(book)), 201


@books_bp.route('/api/users/<int:user_id>/books', methods=['GET'])
def get_user_books(user_id):
    db = get_db()
    user = db.execute('SELECT id FROM users WHERE id = ?', (user_id,)).fetchone()
    if user is None:
        return jsonify({'error': '用户不存在。'}), 404

    rows = db.execute(
        '''SELECT b.id, b.title, b.author, b.isbn, b.cover_url, b.description, b.donated_at,
                  c.name AS category_name
           FROM books b
           LEFT JOIN categories c ON b.category_id = c.id
           WHERE b.user_id = ?
           ORDER BY b.donated_at DESC''',
        (user_id,),
    ).fetchall()
    books = [dict(row) for row in rows]
    return jsonify(books)
