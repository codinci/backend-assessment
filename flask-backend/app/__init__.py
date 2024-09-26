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

    # Check if the environment is development or production
    if env.get('FLASK_ENV') == 'development':
        # Use SQLite in development
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer_orders.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = env.get('DATABASE_URL')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Import and register blueprints (routes and auth)
    from .routes import main_bp
    from .auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
