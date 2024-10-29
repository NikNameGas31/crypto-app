import pytest
from fastapi.testclient import TestClient
from main import app # Импортируйте ваше приложение

client = TestClient(app)

def test_get_prices_empty():
    response = client.get("/prices?ticker=btc_usd")
    assert response.status_code == 200
    assert response.json() == []

def test_get_latest_price_empty():
    response = client.get("/prices/latest?ticker=btc_usd")
    assert response.status_code == 404
    assert response.json() == {"detail": "No data found"}

def test_get_prices_with_data():
    # Добавьте тест для проверки сохраненных данных.
    # Для этого вам нужно запустить клиент или вручную добавить данные в базу.

    # Пример добавления данных (можно сделать через клиент):
    # await save_price('btc_usd', 50000.0)  # Поставьте нужное значение
    # Пример: проверьте, что данные были успешно добавлены

    # Пример запроса
    response = client.get("/prices?ticker=btc_usd")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Убедитесь, что возвращается список

def test_get_latest_price_with_data():
    # Добавьте данные в базу перед проверкой
    # await save_price('btc_usd', 50000.0)  # Поставьте нужное значение

    response = client.get("/prices/latest?ticker=btc_usd")
    assert response.status_code == 200
    assert 'ticker' in response.json()  # Проверьте, что ответ содержит ключ ticker