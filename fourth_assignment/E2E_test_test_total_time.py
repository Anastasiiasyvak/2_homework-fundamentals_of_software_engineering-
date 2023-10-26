import requests

def test_get_total_online_time_user_online():
    user_id = "4c9314d8-75cc-24e6-4443-172c2b0b3f87"
    response = requests.get(f'http://0.0.0.0:8000/api/stats/user/total?user_id={user_id}')
    assert response.status_code == 200
    data = response.json()
    assert "totalTime" in data
    total_time = data["totalTime"]
    assert total_time > 0

def test_get_total_online_time_user_never_online():
    user_id = "e1f2d509-a0c9-f79a-177a-7252e4d72a70"
    response = requests.get(f'http://0.0.0.0:8000/api/stats/user/total?user_id={user_id}')
    assert response.status_code == 200
    data = response.json()
    assert "totalTime" in data
    total_time = data["totalTime"]
    assert total_time == 0

def test_get_total_online_time_invalid_user():
    user_id = "hn5d509-a0c9-f79a-147a-7252e4d75a70" 
    response = requests.get(f'http://0.0.0.0:8000/api/stats/user/total?user_id={user_id}')
    assert response.status_code == 200
    data = response.json()
    assert "totalTime" in data
    total_time = data["totalTime"]
    assert total_time == 0
