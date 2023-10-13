from datetime import datetime
from fastapi.testclient import TestClient
from feature1 import app

client = TestClient(app)


def test_feature1_integration():
    date = datetime(2023, 9, 27, 20, 0)
    response = client.get(f"/api/stats/users?date={date}")

    assert response.status_code == 200
    data = response.json()
    assert "usersOnline" in data


def test_feature2_integration():
    date = datetime(2023, 9, 27, 20, 0)
    user_id = "A4DC2287-B03D-430C-92E8-02216D828709"
    response = client.get(f"/api/stats/user?date={date}&userId={user_id}")

    assert response.status_code == 200
    data = response.json()
    assert "wasUserOnline" in data
    assert "nearestOnlineTime" in data


def test_feature3_integration():
    date = datetime(2025, 9, 27, 20, 0)
    response = client.get(f"/api/predictions/users?date={date}")

    assert response.status_code == 200
    data = response.json()
    assert "onlineUsers" in data


def test_feature4_integration():
    date = datetime(2025, 9, 27, 20, 0)
    user_id = "A4DC2287-B03D-430C-92E8-02216D828709"
    response = client.get(f"/api/predictions/user?date={date}&userId={user_id}&tolerance=0.85")

    assert response.status_code
