from flask import Blueprint, render_template, session, redirect, url_for
from urllib.parse import quote_plus, urlencode
from os import environ as env
import json

# Define a blueprint for the main routes
main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@main_bp.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("main.home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

