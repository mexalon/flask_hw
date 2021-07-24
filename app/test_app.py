import json

import pytest
import main as tested_app
from models import User


@pytest.fixture
def client():
    tested_app.app.config['TESTING'] = True
    app = tested_app.app.test_client()
    return app


def test_get(client):
    r = client.get('/test')
    assert r.json == {'test_me': 'OK!'}


def test_db(client):
    r = client.get('/')
    assert r.json == {'db': 'OK!'}


def test_post_u(client):
    r = client.post('/users', json={"username": "test user for testing", "password": "testuserpassword"})
    assert r.json.get("username") == "test user for testing"
    uid = r.json.get('id')
    test_user = User.query.get(uid)
    test_user.delete()
