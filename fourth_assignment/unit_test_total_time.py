from total_time_was_user_online import calculate_total_online_time

def test_total_online_time_user_online():
    user_id = "4c9314d8-75cc-24e6-4443-172c2b0b3f87"  # існуючий user id
    total_time = calculate_total_online_time(user_id)
    assert total_time > 0

def test_total_online_time_user_never_online():
    user_id = "e1f2d509-a0c9-f79a-177a-7252e4d72a70"  # ніколи не був онлайн
    total_time = calculate_total_online_time(user_id)
    assert total_time == 0

def test_total_online_time_invalid_user():
    user_id = "hn5d509-a0c9-f79a-147a-7252e4d75a70"  # неіснуючий айді
    total_time = calculate_total_online_time(user_id)
    assert total_time == 0
