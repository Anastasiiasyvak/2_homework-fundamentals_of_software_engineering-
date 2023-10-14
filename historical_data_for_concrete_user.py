from datetime import datetime
from fetch_user_data import fetch_user_data

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
