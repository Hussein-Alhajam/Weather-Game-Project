from unittest.mock import patch
from backend.services.auth_service import AuthService

@patch.object(AuthService, 'register_user')
def test_register_user(mock_register, client):
    # Mock return
    mock_register.return_value = {"id": 1, "username": "new_user", "email": "new_user@example.com"}

    payload = {"username": "new_user", "email": "new_user@example.com", "password": "securepassword"}
    response = client.post('/auth/register', json=payload)

    assert response.status_code == 201
    assert response.json["msg"] == "Registration successful"
    mock_register.assert_called_once_with("new_user", "new_user@example.com", "securepassword")

@patch.object(AuthService, 'login_user')
def test_login_user(mock_login, client):
    # Mock return
    mock_login.return_value = {"access_token": "test_token"}

    payload = {"username": "test_user", "password": "securepassword"}
    response = client.post('/auth/login', json=payload)

    assert response.status_code == 200
    assert response.json["access_token"] == "test_token"
    mock_login.assert_called_once_with("test_user", "securepassword")

@patch.object(AuthService, 'google_login')
def test_google_login(mock_google_login, client):
    # Mock return
    mock_google_login.return_value = {"msg": "Google login successful"}

    response = client.get('/auth/login/google')
    assert response.status_code == 200
    assert response.json["msg"] == "Google login successful"
    mock_google_login.assert_called_once()
