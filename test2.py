from datetime import datetime
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_historical_data_for_all_user_integration():
    date = datetime(2023, 9, 27, 20, 0)
    response = client.get(f"/api/stats/users?date={date}")

    assert response.status_code == 200
    data = response.json()

    assert "usersOnline" in data
    users_online = data["usersOnline"]

    assert isinstance(users_online, int)
    assert users_online >= 0


def test_historical_data_for_concrete_user_integration():
    date = datetime(2023, 9, 27, 20, 0)
    user_id = "A4DC2287-B03D-430C-92E8-02216D828709"
    response = client.get(f"/api/stats/user?date={date}&userId={user_id}")

    assert response.status_code == 200
    data = response.json()

    assert "wasUserOnline" in data
    assert "nearestOnlineTime" in data

    was_user_online = data["wasUserOnline"]

    assert isinstance(was_user_online, bool)


def test_prediction_mechanism_on_historical_data_for_user_count_integration():
    date = datetime(2025, 9, 27, 20, 0)
    response = client.get(f"/api/predictions/users?date={date}")

    assert response.status_code == 200
    data = response.json()

    assert "onlineUsers" in data
    online_users = data["onlineUsers"]

    assert isinstance(online_users, int)
    assert online_users >= 0


def test_preduction_mechanism_on_historical_data_concrete_user_integration():
    date = datetime(2025, 9, 27, 20, 0)
    user_id = "A4DC2287-B03D-430C-92E8-02216D828709"
    response = client.get(f"/api/predictions/user?date={date}&userId={user_id}&tolerance=0.85")

    assert response.status_code == 200
    data = response.json()

    assert "willBeOnline" in data
    assert "onlineChance" in data

    will_be_online = data["willBeOnline"]

    assert isinstance(will_be_online, bool)


def test_edge_case_lower_date_limit():
    date = datetime(2000, 1, 1, 0, 0)
    response = client.get(f"/api/stats/users?date={date}")

    assert response.status_code == 200
    data = response.json()

    assert "usersOnline" in data
    users_online = data["usersOnline"]

    assert isinstance(users_online, int)
    assert users_online >= 0


def test_invalid_future_date():
    date = datetime(2030, 1, 1, 0, 0)
    response = client.get(f"/api/stats/users?date={date}")

    assert response.status_code == 400


def test_no_data_scenario():
    date = datetime(2023, 9, 27, 20, 0)

    response = client.get(f"/api/stats/users?date={date}")

    assert response.status_code == 200
    data = response.json()

    assert "usersOnline" in data
    users_online = data["usersOnline"]

    assert isinstance(users_online, int)
    assert users_online == 0
