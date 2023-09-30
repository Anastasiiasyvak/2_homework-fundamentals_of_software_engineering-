import requests
from datetime import datetime, timedelta
import pytz



def last_seen_task(last_seen):
    now = datetime.now(timezone)  
    last_seen = last_seen.split(".")[0]
    last_time_online = datetime.fromisoformat(last_seen)
    last_time_online = last_time_online.replace(tzinfo=pytz.UTC)
    last_time_online = last_time_online.astimezone(timezone)
    time = now - last_time_online

    if time < timedelta(seconds=30):
        return "just now"
    elif time < timedelta(minutes=1):
        return "less than a minute ago"
    elif time < timedelta(minutes=60):
        return "couple of minutes ago"
    elif time < timedelta(minutes=120):
        return "hour ago"
    elif time < timedelta(hours=24):
        return "today"
    elif time < timedelta(hours=48):
        return "yesterday"
    elif time < timedelta(days=7):
        return "this week"
    else:
        return "long time ago"

offset = 0
timezone = pytz.timezone("Europe/Kyiv")

url = f'https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    users = data.get('data', [])

    if users:
        for user in users:
            username = user.get('nickname', 'unknown user')
            last_seen = user.get('lastSeenDate', None)
            if last_seen:
                time_of_visit = last_seen_task(last_seen)
                print(f"{username} was online {time_of_visit}")
            else:
                print(f"{username} is online now")
    else:
        print("User data not found in the API response")
else:
    print(f"Unable to retrieve data. Status code: {response.status_code}")
