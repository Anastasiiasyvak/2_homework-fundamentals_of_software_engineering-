from fastapi import FastAPI, Query
from datetime import datetime
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
@app.get('/api/stats/users')
async def get_user_stats(date: datetime = Query(..., description="Requested date and time")):
    user_data = fetch_user_data(0)

    historical_data = []  

    for user in user_data:
        last_seen = user.get('lastSeenDate', None)
        if last_seen:
            last_seen = last_seen.split('.')[0]
            last_seen_date = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S")

            if last_seen_date <= date:
                historical_data.append({
                    'user_id': user.get('user_id'),
                    'last_seen_date': last_seen_date
                })

    total_users_count = len(user_data)

    print(f"Users Online at {date}: {len(historical_data)}")
    print(f"Total Users: {total_users_count}")

    return {'usersOnline': len(historical_data), 'historicalData': historical_data}

@app.get('/')
async def root(date: datetime = Query(..., description="Requested date and time")):
    user_data = fetch_user_data(0)

    historical_data = []

    for user in user_data:
        last_seen = user.get('lastSeenDate', None)
        if last_seen:
            last_seen = last_seen[:16]
            last_seen_date = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M")

            if last_seen_date <= date:
                historical_data.append({
                    'user_id': user.get('user_id'),
                    'last_seen_date': last_seen_date
                })

    total_users_count = len(user_data)

    print(f"Users Online at {date}: {len(historical_data)}")
    print(f"Total Users: {total_users_count}")

    return {
        'message': "historical data for all user",
        'usersOnline': len(historical_data),
        'historicalData': historical_data,
        'totalUsers': total_users_count
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


#  curl -X GET "http://0.0.0.0:8000/api/stats/users?date=2023-09-27T20:00" вводити в термінал потім дивитись в консоль
