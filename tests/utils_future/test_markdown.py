import unittest

from utils_future import Markdown


class TestCase(unittest.TestCase):
    def test_table(self):
        d_list = [
            {"name": "Alice", "age": 30, "n_score": 95.5},
            {"name": "Bob", "age": 25, "n_score": 88},
        ]
        expected_output = [
            "| name | age | n_score |",
            "| :-- | :-- | --: |",
            "| Alice | 30 | 95.5 |",
            "| Bob | 25 | 88 |",
        ]
        self.assertEqual(Markdown.table(d_list), expected_output)

    def test_row_table(self):
        d_list = [{"name": "Alice", "age": 30, "n_score": 95.5}]
        expected_output = [
            "|   |    |",
            "| :-- | --: |",
            "| name | Alice |",
            "| age | 30 |",
            "| n_score | 95.5 |",
        ]
        self.assertEqual(Markdown.table(d_list), expected_output)

    def test_empty_table(self):
        self.assertEqual(Markdown.table([]), [])
