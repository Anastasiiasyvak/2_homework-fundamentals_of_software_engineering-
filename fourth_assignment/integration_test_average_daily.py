import requests

BASE_URL = "http://localhost:8001"

def test_get_total_online_time():
    user_id = "4c9314d8-75cc-24e6-4443-172c2b0b3f87"
    response = requests.get(f"{BASE_URL}/api/stats/user/total?user_id={user_id}")

    assert response.status_code == 200
    data = response.json()
    assert "totalTime" in data
    assert isinstance(data["totalTime"], (int, float))

def test_get_average_online_time():
    user_id = "4c9314d8-75cc-24e6-4443-172c2b0b3f87"
    response = requests.get(f"{BASE_URL}/api/stats/user/average?user_id={user_id}")

    assert response.status_code == 200
    data = response.json()
    assert "weeklyAverage" in data
    assert "dailyAverage" in data
    assert isinstance(data["weeklyAverage"], (int, float))
    assert isinstance(data["dailyAverage"], (int, float))

if __name__ == "__main__":
    test_get_total_online_time()
    test_get_average_online_time()
