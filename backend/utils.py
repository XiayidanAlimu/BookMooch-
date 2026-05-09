from flask import request
from db import get_db


def get_json_data():
    return request.get_json(silent=True) or {}


def get_token_from_request():
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]

    data = get_json_data()
    return data.get('token')


def get_current_user():
    token = get_token_from_request()
    if not token:
        return None

    db = get_db()
    row = db.execute(
        'SELECT u.id, u.username, u.fullname, u.email FROM sessions s JOIN users u ON s.user_id = u.id WHERE s.token = ?',
        (token,),
    ).fetchone()
    return dict(row) if row else None
