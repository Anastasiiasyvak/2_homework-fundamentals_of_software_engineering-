from average_daily_time import calculate_average_online_time

def test_calculate_average_online_time_user_online():
    user_id = "4c9314d8-75cc-24e6-4443-172c2b0b3f87"
    last_seen_dates = ["2023-10-25T12:00:00.000000", "2023-10-24T12:00:00.000000"]

    weekly_average, daily_average = calculate_average_online_time(user_id, [user_id], last_seen_dates)
    assert weekly_average > 0
    assert daily_average > 0



def test_calculate_average_online_time_user_never_online():
    user_id = "e1f2d509-a0c9-f79a-177a-7252e4d72a70"

    weekly_average, daily_average = calculate_average_online_time(user_id, [], [])
    assert weekly_average == 0
    assert daily_average == 0
