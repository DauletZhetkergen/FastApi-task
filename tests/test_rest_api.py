import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_signup(client):
    payload = {
        "username": "test",
        "password": "test"
    }
    res = client.post("/api/user/sign-up", json=payload)
    assert res.status_code == 200
    assert res.json()["username"] == "test"


def test_auth(client):
    payload = {
        "username": "test",
        "password": "test"

    }
    res = client.post("/api/user/auth", data=payload)
    assert res.status_code == 200


@pytest.fixture
def auth_token(client):
    payload = {
        "username": "daulet",
        "password": "123"
    }
    res = client.post("api/user/auth", data=payload)
    assert res.status_code == 200
    token = res.json().get("access_token")
    assert token is not None
    return token


def test_order_id(client, auth_token):  # —начала берем токен потом уже вызываем
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("api/orders/3", headers=headers)
    assert res.status_code == 200


def test_order_create(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    payload = {
        "customer_name": "test",
        "products": [
            {
                "product_id": 1,
                "quantity": 1
            }
        ]
    }
    res = client.post("/api/orders", headers=headers, json=payload)
    assert res.status_code == 200


def test_get_orders(client, auth_token):  # —начала берем токен потом уже вызываем
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("api/orders?status=pending", headers=headers)
    assert res.status_code == 200


def test_update_orders(client, auth_token):  # ѕомен€йте order_id на свой а то будет ругатьс€ что заказ не ваш
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.put("/api/orders?order_id=3&status=pending", headers=headers)
    assert res.status_code == 200


def test_delete_order(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    order_id = 6#тоже помен€йте на свой сначала создайте заказ чтобы протестировать
    res = client.delete(f"/api/orders?order_id={order_id}", headers=headers)
    assert res.status_code == 200
