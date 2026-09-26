from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["application"] == "E-Commerce Order Platform"


def test_get_products():
    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_product():
    response = client.post(
        "/products",
        json={
            "name": "Test Product",
            "price": 1000,
            "stock": 10
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Product"
    assert data["price"] == 1000
    assert data["stock"] == 10


def test_get_orders():
    response = client.get("/orders")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_existing_order():
    response = client.get("/orders/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["status"] == "PENDING"
    assert "items" in data


def test_get_nonexistent_order():
    response = client.get("/orders/999999")

    assert response.status_code == 404
