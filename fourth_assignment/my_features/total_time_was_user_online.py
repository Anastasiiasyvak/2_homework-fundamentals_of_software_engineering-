from fastapi import FastAPI, Query
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
def calculate_total_online_time(user_id: str, offset: int = Query(0, description="Offset for fetching user data")):
    user_data = fetch_user_data(offset)

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

@app.get("/api/stats/user/total")
async def get_total_online_time(user_id: str, offset: int = Query(0, description="Offset for fetching user data")):
    total_time = calculate_total_online_time(user_id, offset)

    return {"totalTime": total_time}
