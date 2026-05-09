from flask import Flask
from flask_cors import CORS
from db import init_db, close_db
from blueprints.auth import auth_bp
from blueprints.books import books_bp
from blueprints.orders import orders_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(books_bp)
app.register_blueprint(orders_bp)
app.teardown_appcontext(close_db)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
