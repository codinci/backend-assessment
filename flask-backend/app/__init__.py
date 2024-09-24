from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import environ as env

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask app and database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = env.get("APP_SECRET_KEY")

    # Database configuration (SQLite for local dev, PostgreSQL in prod)
    if env.get('FLASK_ENV') == 'production':
        app.config['SQLALCHEMY_DATABASE_URI'] = env.get('DATABASE_URL')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer_orders.db'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Import and register blueprints (routes and auth)
    from .routes import main_bp
    from .auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
