import os
import sqlite3
from flask import g

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'books.db')

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

CREATE TABLE IF NOT EXISTS wishlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(book_id) REFERENCES books(id),
    UNIQUE(user_id, book_id)
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    recipient_name TEXT NOT NULL,
    address TEXT NOT NULL,
    phone TEXT,
    note TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(book_id) REFERENCES books(id)
);
"""

DEFAULT_CATEGORIES = [
    '儿童读物',
    '文学小说',
    '历史传记',
    '科技教育',
    '艺术设计',
]

DEFAULT_USERS = [
    ('alice', 'alice', 'Alice Chen', 'alice@example.com'),
    ('bob', 'password', 'Bob Wang', 'bob@example.com'),
]


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        g.db = db
    return db


def close_db(error=None):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def apply_book_migration(db):
    rows = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'").fetchall()
    if not rows:
        return

    columns = [row[1] for row in db.execute('PRAGMA table_info(books)').fetchall()]
    if 'isbn' not in columns:
        db.execute('ALTER TABLE books ADD COLUMN isbn TEXT')
    if 'cover_url' not in columns:
        db.execute('ALTER TABLE books ADD COLUMN cover_url TEXT')
    if 'category_id' not in columns:
        db.execute('ALTER TABLE books ADD COLUMN category_id INTEGER')
    if 'user_id' not in columns:
        db.execute('ALTER TABLE books ADD COLUMN user_id INTEGER')


def init_db():
    db = get_db()
    db.executescript(SQL_SCHEMA)
    apply_book_migration(db)

    for category in DEFAULT_CATEGORIES:
        db.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (category,))

    for username, password, fullname, email in DEFAULT_USERS:
        db.execute(
            'INSERT OR IGNORE INTO users (username, password, fullname, email) VALUES (?, ?, ?, ?)',
            (username, password, fullname, email),
        )

    db.commit()
