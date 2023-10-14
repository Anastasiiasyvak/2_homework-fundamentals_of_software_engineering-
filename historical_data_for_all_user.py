import fetch_user_data
from datetime import datetime
import requests


def Historical_data_for_all_user(date):
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

    return {
        'usersOnline': len(historical_data),
        'historicalData': historical_data,
        'totalUsers': total_users_count
    }
