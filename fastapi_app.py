from datetime import datetime
from fastapi import FastAPI, Query
from historical_data_for_all_user import Historical_data_for_all_user
from fetch_user_data import fetch_user_data
from historical_data_for_concrete_user import historical_data_for_concrete_user
from prediction_mechanism import prediction_mechanism_for_users_count, prediction_mechanish_for_concrete_user

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
    if chosen_feature == 'historical data for all users':
        return Historical_data_for_all_user(date)
    elif chosen_feature == 'historical data for concrete user':
        print("Please enter user_id:")
        user_id = input()
        return historical_data_for_concrete_user(date, user_id)
    elif chosen_feature == 'prediction mechanism for user count':
        return prediction_mechanism_for_users_count(date)
    elif chosen_feature == 'prediction mechanism for concrete user':
        print("Please enter user_id:")
        user_id = input()
        return prediction_mechanish_for_concrete_user(date, user_id)
    else:
        return {'error': 'Invalid feature name'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
