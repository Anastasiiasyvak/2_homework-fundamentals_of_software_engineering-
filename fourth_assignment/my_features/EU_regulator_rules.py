from fastapi import FastAPI
import requests

app = FastAPI()

def fetch_user_data(offset):
    url = f'https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        return []

@app.post("/api/user/forget")
async def forget_user(user_id: str):
    user_data = fetch_user_data(0)

    user_found = False
    for user in user_data:
        if user.get('userId') == user_id:
            user_data.remove(user)
            user_found = True
            break

    if user_found:
        response_message = f"User {user_id} data has been deleted as per GDPR regulations."
        print(f"User {user_id} data has been deleted.")
    else:
        response_message = f"User {user_id} not found."
        print(f"User {user_id} not found.")

    return {"userId": user_id, "message": response_message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
