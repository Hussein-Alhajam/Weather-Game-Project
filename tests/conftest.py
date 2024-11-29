import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from backend.app import create_app  
from backend.extensions import db
from backend.models.user_model import User 

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'test-secret-key',
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def seed_user(app):
    """Seed a test user into the database and return the user and access token."""
    with app.app_context():
        user = User(username='testuser', email='testuser@example.com', password='securepassword')
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.id)
        return user, access_token

@pytest.fixture
def auth_headers(seed_user):
    """Generate headers with JWT access token for authenticated requests."""
    _, access_token = seed_user
    return {"Authorization": f"Bearer {access_token}"}
