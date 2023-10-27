import pytest
from fastapi.testclient import TestClient
from fourth_assignment.my_features.EU_regulator_rules import app, fetch_user_data

client = TestClient(app)

def test_fetch_user_data():
    def mock_get(url):
        class MockResponse:
            status_code = 200
            json_data = {"data": [{"userId": "user1"}, {"userId": "user2"}]}

            def json(self):
                return self.json_data

        return MockResponse()

    offset = 0
    data = fetch_user_data(offset)
    assert data == [{"userId": "user1"}, {"userId": "user2"}]

def test_forget_user():
    app.state.user_data = [{"userId": "user1"}, {"userId": "user2"}]

    user_id = "4c9314d8-75cc-24e6-4443-172c2b0b3f87"
    response = client.post("/api/user/forget", json={"user_id": user_id})
    assert response.status_code == 200
    assert response.json() == {"userId": user_id, "message": f"User {user_id} data has been deleted as per GDPR regulations."}
    assert {"userId": "user1"} not in app.state.user_data

    user_id = "e1f2d509-a0c9-f79a-177a-7252e4d72a70"
    response = client.post("/api/user/forget", json={"user_id": user_id})
    assert response.status_code == 200
    assert response.json() == {"userId": user_id, "message": f"User {user_id} not found"}
    assert {"userId": "non_existent_user"} not in app.state.user_data

if __name__ == "__main__":
    pytest.main()
