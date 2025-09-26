import unittest

from utils_future.Format import Format


class TestCase(unittest.TestCase):
    def test_badge(self):
        for x, expected_result in [
            ("hello-world", "hello--world"),
            ("hello world", "hello_world"),
            ("hello-world test", "hello--world_test"),
        ]:

            self.assertEqual(Format.badge(x), expected_result)

    def test_and_list(self):
        for x, expected_result in [
            ([], ""),
            (["apple"], "apple"),
            (["apple", "banana"], "apple & banana"),
            (["apple", "banana", "cherry"], "apple, banana & cherry"),
            (
                ["apple", "banana", "cherry", "date", "guava", "mango"],
                "apple, banana, cherry, date, guava & 1 more",
            ),
        ]:

            self.assertEqual(Format.and_list(x), expected_result)

    def test_title(self):
        for x, expected_result in [
            ("hello_world", "Hello World"),
            ("Lk_news", "#SriLanka 🇱🇰 News"),
            ("test_Lk_case", "Test #SriLanka 🇱🇰 Case"),
        ]:

            self.assertEqual(Format.title(x), expected_result)
