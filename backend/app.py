from flask import Flask, jsonify, request, g
from flask_cors import CORS
import sqlite3
import os
import uuid
import requests

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "books.db")

app = Flask(__name__)
CORS(app)

SQL_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    fullname TEXT NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT,
    cover_url TEXT,
    description TEXT,
    category_id INTEGER,
    user_id INTEGER,
    donated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(category_id) REFERENCES categories(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
"""

DEFAULT_CATEGORIES = [
    "儿童读物",
    "文学小说",
    "历史传记",
    "科技教育",
    "艺术设计",
]

DEFAULT_USERS = [
    ("alice", "password", "Alice Chen", "alice@example.com"),
    ("bob", "password", "Bob Wang", "bob@example.com"),
]


def get_db():
    db = getattr(g, "db", None)
    if db is None:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        g.db = db
    return db


@app.teardown_appcontext
def close_db(error=None):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()


def apply_book_migration(db):
    rows = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'").fetchall()
    if not rows:
        return

    columns = [row[1] for row in db.execute("PRAGMA table_info(books)").fetchall()]
    if "isbn" not in columns:
        db.execute("ALTER TABLE books ADD COLUMN isbn TEXT")
    if "cover_url" not in columns:
        db.execute("ALTER TABLE books ADD COLUMN cover_url TEXT")
    if "category_id" not in columns:
        db.execute("ALTER TABLE books ADD COLUMN category_id INTEGER")
    if "user_id" not in columns:
        db.execute("ALTER TABLE books ADD COLUMN user_id INTEGER")


def init_db():
    db = get_db()
    db.executescript(SQL_SCHEMA)
    apply_book_migration(db)

    for category in DEFAULT_CATEGORIES:
        db.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category,))

    for username, password, fullname, email in DEFAULT_USERS:
        db.execute(
            "INSERT OR IGNORE INTO users (username, password, fullname, email) VALUES (?, ?, ?, ?)",
            (username, password, fullname, email),
        )

    db.commit()


def get_json_data():
    return request.get_json(silent=True) or {}


def get_token_from_request():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]
    data = get_json_data()
    return data.get("token")


def get_current_user():
    token = get_token_from_request()
    if not token:
        return None

    db = get_db()
    row = db.execute(
        "SELECT u.id, u.username, u.fullname, u.email FROM sessions s JOIN users u ON s.user_id = u.id WHERE s.token = ?",
        (token,),
    ).fetchone()
    return dict(row) if row else None


# @app.before_first_request
# def setup_database():
#     init_db()


@app.route("/api/categories", methods=["GET"])
def get_categories():
    try:
        db = get_db()
        rows = db.execute("SELECT id, name FROM categories ORDER BY id").fetchall()
        return jsonify([dict(row) for row in rows])
    except Exception as e:
        app.logger.error("Error in /api/categories", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/book-search", methods=["GET"])
def book_search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    try:
        response = requests.get(
            "https://openlibrary.org/search.json",
            params={"q": query, "limit": 12},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        results = []
        for idx, doc in enumerate(data.get("docs", [])):
            title = doc.get("title") or ""
            author = (doc.get("author_name") or [""])[0]
            isbn_list = doc.get("isbn") or []
            isbn = isbn_list[0] if isbn_list else ""
            cover_id = doc.get("cover_i")
            cover_url = None
            if cover_id:
                cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
            elif isbn:
                cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"

            results.append({
                "id": doc.get("key", f"openlib-{idx}"),
                "title": title,
                "author": author,
                "isbn": isbn,
                "cover_url": cover_url,
            })
        return jsonify(results)
    except Exception as e:
        app.logger.error("Error in /api/book-search", exc_info=True)
        return jsonify({"error": "图书搜索接口失败，请稍后重试。"}), 500


@app.route("/api/login", methods=["POST"])
def login():
    data = get_json_data()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空。"}), 400

    db = get_db()
    user = db.execute(
        "SELECT id, username, fullname, email FROM users WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    if user is None:
        return jsonify({"error": "用户名或密码错误。"}), 401

    token = str(uuid.uuid4())
    db.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, user["id"]))
    db.commit()

    return jsonify({
        "token": token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "fullname": user["fullname"],
            "email": user["email"],
        },
    })


@app.route("/api/register", methods=["POST"])
def register():
    data = get_json_data()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    fullname = data.get("fullname", "").strip()
    email = data.get("email", "").strip()

    if not username or not password or not fullname:
        return jsonify({"error": "用户名、密码和真实姓名不能为空。"}), 400

    db = get_db()
    try:
        cursor = db.execute(
            "INSERT INTO users (username, password, fullname, email) VALUES (?, ?, ?, ?)",
            (username, password, fullname, email),
        )
        db.commit()
        user_id = cursor.lastrowid
        user = db.execute("SELECT id, username, fullname, email FROM users WHERE id = ?", (user_id,)).fetchone()
        return jsonify(dict(user)), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "用户名已存在。"}), 409


@app.route("/api/logout", methods=["POST"])
def logout():
    token = get_token_from_request()
    if token:
        db = get_db()
        db.execute("DELETE FROM sessions WHERE token = ?", (token,))
        db.commit()
    return jsonify({"success": True})


@app.route("/api/me", methods=["GET"])
def me():
    user = get_current_user()
    if user is None:
        return jsonify({"error": "未登录。"}), 401

    db = get_db()
    count = db.execute("SELECT COUNT(*) AS total FROM books WHERE user_id = ?", (user["id"],)).fetchone()["total"]
    user["donated_books_count"] = count
    return jsonify(user)


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    db = get_db()
    user = db.execute(
        "SELECT id, username, fullname, email, created_at FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    if user is None:
        return jsonify({"error": "用户不存在。"}), 404

    donated_count = db.execute("SELECT COUNT(*) AS total FROM books WHERE user_id = ?", (user_id,)).fetchone()["total"]
    result = dict(user)
    result["donated_books_count"] = donated_count
    return jsonify(result)


@app.route("/api/users/<int:user_id>/books", methods=["GET"])
def get_user_books(user_id):
    db = get_db()
    user = db.execute("SELECT id FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        return jsonify({"error": "用户不存在。"}), 404

    rows = db.execute(
        "SELECT b.id, b.title, b.author, b.isbn, b.cover_url, b.description, b.donated_at, c.name AS category_name FROM books b LEFT JOIN categories c ON b.category_id = c.id WHERE b.user_id = ? ORDER BY b.donated_at DESC",
        (user_id,),
    ).fetchall()
    books = [dict(row) for row in rows]
    return jsonify(books)


@app.route("/api/books", methods=["GET"])
def get_books():
    db = get_db()
    category_id = request.args.get("category_id")
    query = "SELECT b.id, b.title, b.author, b.isbn, b.cover_url, b.description, b.donated_at, c.name AS category_name, u.fullname AS donor FROM books b LEFT JOIN categories c ON b.category_id = c.id LEFT JOIN users u ON b.user_id = u.id"
    params = []
    if category_id:
        query += " WHERE b.category_id = ?"
        params.append(category_id)
    query += " ORDER BY b.donated_at DESC"

    rows = db.execute(query, params).fetchall()
    books = [dict(row) for row in rows]
    return jsonify(books)


@app.route("/api/books", methods=["POST"])
def add_book():
    user = get_current_user()
    if user is None:
        return jsonify({"error": "请先登录后提交捐书。"}), 401

    data = get_json_data()
    title = (data.get("title") or "").strip()
    author = (data.get("author") or "").strip()
    isbn = (data.get("isbn") or "").strip()
    description = (data.get("description") or "").strip()
    category_id = data.get("category_id")

    if not title or not author:
        return jsonify({"error": "标题和作者为必填字段。"}), 400

    db = get_db()
    if category_id:
        category = db.execute("SELECT id FROM categories WHERE id = ?", (category_id,)).fetchone()
        if category is None:
            return jsonify({"error": "所选分类不存在。"}), 400

    cursor = db.execute(
        "INSERT INTO books (title, author, isbn, cover_url, description, category_id, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (title, author, isbn, data.get("cover_url"), description, category_id, user["id"]),
    )
    db.commit()

    book_id = cursor.lastrowid
    book = db.execute(
        "SELECT b.id, b.title, b.author, b.isbn, b.cover_url, b.description, b.donated_at, c.name AS category_name, u.fullname AS donor FROM books b LEFT JOIN categories c ON b.category_id = c.id LEFT JOIN users u ON b.user_id = u.id WHERE b.id = ?",
        (book_id,),
    ).fetchone()
    return jsonify(dict(book)), 201

def add_isbn_column():
    db = get_db()
    # 检查是否已存在 isbn 列
    columns = [row[1] for row in db.execute("PRAGMA table_info(books)").fetchall()]
    if 'isbn' not in columns:
        db.execute("ALTER TABLE books ADD COLUMN isbn TEXT")


if __name__ == "__main__":
    with app.app_context():
        init_db()
        add_isbn_column()
    app.run(host="0.0.0.0", port=5000, debug=True)
