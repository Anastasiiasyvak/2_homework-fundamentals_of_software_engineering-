from fastapi import FastAPI
import requests
from datetime import datetime

app = FastAPI()

def fetch_user_data(offset):
    url = f'https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        return []

@app.get("/api/stats/user/total")
async def get_total_online_time(user_id: str):
    total_time = calculate_total_online_time(user_id)

    print(f"Total time for user {user_id}: {total_time} seconds")

    return {"totalTime": total_time}

def calculate_total_online_time(user_id: str):
    user_data = fetch_user_data(0)

    total_time = 0

    for user in user_data:
        if user.get('userId') == user_id:
            last_seen_date = user.get('lastSeenDate')
            if last_seen_date:
                last_seen_datetime = datetime.fromisoformat(last_seen_date[:-1])
                current_datetime = datetime.now()
                time_online = current_datetime - last_seen_datetime
                total_time = time_online.total_seconds()
                break

    return total_time

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
