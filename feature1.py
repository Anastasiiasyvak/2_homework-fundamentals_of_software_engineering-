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


def feature1(date):
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


def feature2(date, user_id):
    user_data = fetch_user_data(0)

    found_user = None
    for user in user_data:
        if user.get('userId') == user_id:
            found_user = user
            break

    if found_user is None:
        print("User not found.")
        return {'wasUserOnline': None, 'nearestOnlineTime': None}

    last_seen = found_user.get('lastSeenDate', None)
    if last_seen:
        last_seen = last_seen.split('.')[0]
        last_seen_date = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S")

        was_user_online = last_seen_date <= date

        nearest_online_time = None
        for user in user_data:
            if user.get('userId') == user_id:
                continue
            user_last_seen = user.get('lastSeenDate', None)
            if user_last_seen:
                user_last_seen = user_last_seen.split('.')[0]
                user_last_seen_date = datetime.strptime(user_last_seen, "%Y-%m-%dT%H:%M:%S")
                if user_last_seen_date > date:
                    if nearest_online_time is None or user_last_seen_date < nearest_online_time:
                        nearest_online_time = user_last_seen_date

        print(f"User {user_id} was online at {date}: {was_user_online}")
        if nearest_online_time:
            print(f"Nearest online time for user {user_id}: {nearest_online_time}")
        else:
            print(f"User {user_id} has no other online records.")

        return {'wasUserOnline': was_user_online, 'nearestOnlineTime': nearest_online_time}


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


@app.get('/api/stats')
async def choose_feature(date: datetime = Query(..., description="Requested date and time")):
    print("Which feature would you like to execute? (feature1/feature2)")
    chosen_feature = input()
    if chosen_feature == 'feature1':
        return feature1(date)
    elif chosen_feature == 'feature2':
        print("Please enter user_id:")
        user_id = input()
        return feature2(date, user_id)
    else:
        return {'error': 'Invalid feature name'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
