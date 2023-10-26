from fastapi.testclient import TestClient
from EU_regulator_rules import app

client = TestClient(app)

def test_forget_user_integration():
    user_id = "e1f2d509-a0c9-f79a-177a-7252e4d72a70"
    response = client.post("/api/user/forget", json={"user_id": user_id})

    assert response.status_code == 200
    assert response.json() == {"userId": user_id, "message": f"User {user_id} not found"}

    app.state.user_data.append({"userId": user_id})

    response = client.post("/api/user/forget", json={"user_id": user_id})

    assert response.status_code == 200
    assert response.json() == {"userId": user_id, "message": f"User {user_id} data has been deleted as per GDPR regulations."}
    assert {"userId": user_id} not in app.state.user_data

if __name__ == "__main__":
    import pytest
    pytest.main()
