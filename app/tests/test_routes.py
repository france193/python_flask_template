import pytest
from ..main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_register(client):
    data = {
        'email': 'test@example.com',
        'password': 'test123',
        'full_name': 'Test User'
    }
    response = client.post('/register', json=data)
    assert response.status_code == 201
    assert b'User registered successfully' in response.data


def test_login(client):
    data = {
        'email': 'test@example.com',
        'password': 'test123'
    }
    response = client.post('/login', json=data)
    assert response.status_code == 200
    assert b'token' in response.data


def test_2fa(client):
    data = {
        'email': 'test@example.com',
        'otp': '123456'  # Assuming this OTP is generated and sent to the user's email
    }
    response = client.post('/2fa', json=data)
    assert response.status_code == 200
    assert b'token' in response.data
