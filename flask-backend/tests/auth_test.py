import os
import pytest
from flask import session
from app import create_app, db
from app.auth import init_oauth


@pytest.fixture
def app():
    # Set test environment variables for Auth0
    os.environ["AUTH0_CLIENT_ID"] = "test_client_id"
    os.environ["AUTH0_CLIENT_SECRET"] = "test_client_secret"
    os.environ["AUTH0_DOMAIN"] = "test.auth0.com"

    # Create a test client
    app = create_app()
    with app.app_context():
        init_oauth(app)  # Initialize OAuth here
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def init_database(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


def test_login_nonce_in_session(client):
    # Simulate a request to the login route
    with client:
        client.get('/login')

        # Check that nonce is stored in the session
        assert 'nonce' in session


