import unittest
from datetime import datetime, timedelta
import pytz
from main import last_seen_task


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


if __name__ == '__main__':
    unittest.main()