from datetime import datetime
from fetch_user_data import fetch_user_data
from historical_data_for_concrete_user import historical_data_for_concrete_user

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
    user_historical_data = historical_data_for_concrete_user(date, userId)
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
