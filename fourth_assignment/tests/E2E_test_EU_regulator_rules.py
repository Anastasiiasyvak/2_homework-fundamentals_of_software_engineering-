import requests

BASE_URL = "http://localhost:8002"

def test_e2e_forget_user():
    user_id = "e1f2d509-a0c9-f79a-177a-7252e4d72a70"
    response = requests.post(f"{BASE_URL}/api/user/forget", json={"user_id": user_id})

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["userId"] == user_id
    assert "not found" in response_data["message"]

    user_id = "4c9314d8-75cc-24e6-4443-172c2b0b3f87"
    response = requests.post(f"{BASE_URL}/api/user/forget", json={"user_id": user_id})

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["userId"] == user_id
    assert "has been deleted" in response_data["message"]

    response = requests.post(f"{BASE_URL}/api/user/forget", json={"user_id": user_id})

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["userId"] == user_id
    assert "has been deleted" in response_data["message"]

if __name__ == "__main__":
    test_e2e_forget_user()
