import unittest
from datetime import datetime, timedelta
import pytz
from unittest.mock import patch, Mock
from main import last_seen_task, get_user_data


class TestLastSeenTask(unittest.TestCase):
    def test_last_seen_just_now(self):
        now = datetime.now(pytz.timezone("Europe/Kyiv"))
        thirty_seconds_ago = now - timedelta(seconds=30)

        self.assertEqual(last_seen_task(thirty_seconds_ago.isoformat()), "just now")

    def test_last_seen_less_than_a_minute_ago(self):
        now = datetime.now(pytz.timezone("Europe/Kyiv"))
        one_minute_ago = now - timedelta(minutes=1)

        self.assertEqual(last_seen_task(one_minute_ago.isoformat()), "less than a minute ago")

    def test_last_seen_couple_of_minutes_ago(self):
        now = datetime.now(pytz.timezone("Europe/Kyiv"))
        fifty_nine_minutes_ago = now - timedelta(minutes=59)

        self.assertEqual(last_seen_task(fifty_nine_minutes_ago.isoformat()), "couple of minutes ago")

    def test_last_seen_hour_ago(self):
        now = datetime.now(pytz.timezone("Europe/Kyiv"))
        two_hours_ago = now - timedelta(hours=2)

        self.assertEqual(last_seen_task(two_hours_ago.isoformat()), "hour ago")

    def test_last_seen_today(self):
        now = datetime.now(pytz.timezone("Europe/Kyiv"))
        three_hours_ago = now - timedelta(hours=3)

        self.assertEqual(last_seen_task(three_hours_ago.isoformat()), "today")

    def test_last_seen_yesterday(self):
        now = datetime.now(pytz.timezone("Europe/Kyiv"))
        yesterday = now - timedelta(days=1)

        self.assertEqual(last_seen_task(yesterday.isoformat()), "yesterday")

    def test_last_seen_this_week(self):
        now = datetime.now(pytz.timezone("Europe/Kyiv"))
        six_days_ago = now - timedelta(days=6)

        self.assertEqual(last_seen_task(six_days_ago.isoformat()), "this week")

    def test_last_seen_long_time_ago(self):
        now = datetime.now(pytz.timezone("Europe/Kyiv"))
        ten_days_ago = now - timedelta(days=10)

        self.assertEqual(last_seen_task(ten_days_ago.isoformat()), "long time ago")


class TestGetUserData(unittest.TestCase):
    @patch('main.fetch_user_data')
    def test_get_user_data_single_page(self, mock_fetch_user_data):
        mock_response = {'data': [{'nickname': 'first_user', 'lastSeenDate': '2023-10-01T12:00:00Z'}]}
        mock_fetch_user_data.side_effect = [mock_response, []]

        user_data = get_user_data()

        self.assertEqual(len(user_data), 1)
        self.assertEqual(user_data[0]['nickname'], 'first_user')

    @patch('main.fetch_user_data')
    def test_get_user_data_multiple_pages(self, mock_fetch_user_data):
        mock_response1 = {'data': [{'nickname': 'first_user', 'lastSeenDate': '2023-10-01T12:00:00Z'}]}
        mock_response2 = {'data': [{'nickname': 'second_user', 'lastSeenDate': '2023-10-01T13:00:00Z'}]}
        mock_response3 = {}
        mock_fetch_user_data.side_effect = [mock_response1, mock_response2, mock_response3]

        user_data = get_user_data()

        self.assertEqual(len(user_data), 2)
        self.assertEqual(user_data[0]['nickname'], 'first_user')
        self.assertEqual(user_data[1]['nickname'], 'second_user')


if __name__ == '__main__':
    unittest.main()
