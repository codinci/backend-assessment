import secrets
from flask import Blueprint, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from os import environ as env
from urllib.parse import quote_plus, urlencode
from .models import User
from . import db

# Define a blueprint for the auth routes
auth_bp = Blueprint('auth', __name__)

oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)

    oauth.register(
        "auth0",
        client_id=env.get("AUTH0_CLIENT_ID"),
        client_secret=env.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    )

@auth_bp.route("/login")
def login():
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True),
        nonce=nonce
    )

@auth_bp.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    nonce = session.get('nonce')

    if not nonce:
        return "Error: Nonce not found in session", 400

    user_info = oauth.auth0.parse_id_token(token, nonce=nonce)

    email = user_info.get("email")
    name = user_info.get("name")

    existing_user = User.query.filter_by(email=email).first()

    if not existing_user:
        new_user = User(email=email, name=name)
        db.session.add(new_user)
        db.session.commit()

    session["user"] = token
    return redirect(url_for("main.home"))
