import requests
from datetime import datetime, timedelta

def test_get_total_online_time_integration():

    test_user_id = "test_user"
    last_seen_time = (datetime.now() - timedelta(minutes=10)).isoformat()

    add_user_url = f'http://0.0.0.0:8000/api/add_user?userId={test_user_id}&lastSeenDate={last_seen_time}'
    add_user_response = requests.post(add_user_url)
    assert add_user_response.status_code == 200

    response = requests.get(f'http://0.0.0.0:8000/api/stats/user/total?user_id={test_user_id}')
    assert response.status_code == 200
    data = response.json()
    assert "totalTime" in data
    total_time = data["totalTime"]
    assert total_time > 0

    delete_user_url = f'http://0.0.0.0:8000/api/delete_user?userId={test_user_id}'
    delete_user_response = requests.post(delete_user_url)
    assert delete_user_response.status_code == 200
