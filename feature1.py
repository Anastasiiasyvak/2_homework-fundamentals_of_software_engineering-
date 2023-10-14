from datetime import datetime
import requests

def fetch_user_data(offset):
    url = f'https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        return []

def get_user_historical_data(user_id, date):
    user_data = fetch_user_data(0)
    user_historical_data = []

    for user in user_data:
        if user.get('userId') == user_id:
            last_seen = user.get('lastSeenDate', None)
            if last_seen:
                last_seen = last_seen.split('.')[0]
                last_seen_date = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S")

                if last_seen_date <= date:
                    user_historical_data.append({
                        'user_id': user.get('userId'),
                        'last_seen_date': last_seen_date
                    })

    return user_historical_data

def Historical_data_for_all_users(date):
    user_data = fetch_user_data(0)
    historical_data = []

    for user in user_data:
        last_seen = user.get('lastSeenDate', None)
        if last_seen:
            last_seen = last_seen.split('.')[0]
            last_seen_date = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S")

            if last_seen_date <= date:
                historical_data.append({
                    'user_id': user.get('userId'),
                    'last_seen_date': last_seen_date
                })

    total_users_count = len(user_data)

    print(f"Users Online at {date}: {len(historical_data)}")
    print(f"Total Users: {total_users_count}")

    return {'usersOnline': len(historical_data), 'historicalData': historical_data}

def historical_data_for_concrete_user(date, user_id):
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

def prediction_mechanism_for_users_count(date):
    user_data = fetch_user_data(0)

    online_users_count = 0
    online_users_records = 0

    for user in user_data:
        last_seen = user.get('lastSeenDate', None)
        if last_seen:
            last_seen = last_seen.split('.')[0]
            last_seen_date = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S")

            if last_seen_date.weekday() == date.weekday() and last_seen_date.hour == date.hour:
                online_users_count += 1
                online_users_records += 1

    if online_users_records > 0:
        average_online_users = online_users_count / online_users_records
    else:
        average_online_users = 0

    print(f"Predicted online users at {date}: {int(average_online_users)}")

    return {'onlineUsers': int(average_online_users)}

def prediction_mechanish_for_concrete_user(date, userId):
    user_historical_data = get_user_historical_data(userId, date)
    total_weeks = len(user_historical_data)

    if total_weeks == 0:
        online_chance = 0
    else:
        online_chance = len(user_historical_data) / total_weeks

    will_be_online = online_chance > 0.85

    print(f"User {userId} online chance on {date}: {online_chance}")
    print(f"User {userId} will be online on {date}: {will_be_online}")

    return {
        "willBeOnline": will_be_online,
        "onlineChance": online_chance
    }

from fastapi import FastAPI, Query

app = FastAPI()

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
                    'user_id': user.get('userId'),
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
    print("Which feature would you like to execute? (feature1/feature2/feature3/feature4)")
    chosen_feature = input()
    if chosen_feature == 'feature1':
        return Historical_data_for_all_users(date)
    elif chosen_feature == 'feature2':
        print("Please enter user_id:")
        user_id = input()
        return historical_data_for_concrete_user(date, user_id)
    elif chosen_feature == 'feature3':
        return prediction_mechanism_for_users_count(date)
    elif chosen_feature == 'feature4':
        print("Please enter user_id:")
        user_id = input()
        return prediction_mechanish_for_concrete_user(date, user_id)
    else:
        return {'error': 'Invalid feature name'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

#  curl -X GET "http://0.0.0.0:8000/api/stats?date=2023-09-27T20:00"
