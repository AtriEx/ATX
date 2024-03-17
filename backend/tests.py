from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_buy_order():
    response = client.get("/qb")
    assert response.status_code == 200
    # Check if market_open check works
    # Check if buy order receives proper data
    # Check if order can be fulfilled
    # Check 3 different outcomes for prices when stock is bought/sold
