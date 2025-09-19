import unittest

from utils_future.Parse import Parse


class TestCase(unittest.TestCase):
    def test_time_str(self):
        for x, expected_result in [
            ("2023-10-01 12:30", "2023-10-01 12:30"),
            ("2023-10-01T12:30:00Z", "2023-10-01 12:30"),
            ("October 1, 2023, 12:30 PM", "2023-10-01 12:30"),
            ("2023/10/01 12:30:00", "2023-10-01 12:30"),
            ("01 Oct 2023 12:30", "2023-10-01 12:30"),
        ]:

            self.assertEqual(Parse.time_str(x), expected_result)
