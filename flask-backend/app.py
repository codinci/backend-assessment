
import json
import secrets
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer_orders.db'

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))

    def __init__(self, email, name):
        self.email = email
        self.name = name

#OAuth Configuration

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)


@app.route("/login")
def login():
    # Generate a random nonce and store it in the session
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True),
        nonce=nonce
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()

 	# Retrieve the nonce from the session
    nonce = session.get('nonce')

    if not nonce:
        return "Error: Nonce not found in session", 400

    user_info = oauth.auth0.parse_id_token(token, nonce=nonce)

    email = user_info.get("email")
    name = user_info.get("name")

    # Check if user exists
    existing_user = User.query.filter_by(email=email).first()

    if not existing_user:
        new_user = User(email=email, name=name)
        db.session.add(new_user)
        db.session.commit()

	#Store user session
    session["user"] = token
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=env.get("PORT", 5000))
