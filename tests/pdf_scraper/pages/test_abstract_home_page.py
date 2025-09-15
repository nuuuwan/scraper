import unittest

from pdf_scraper import AbstractHomePage


class TestCase(unittest.TestCase):
    def test_method(self):
        page = AbstractHomePage(url="http://example.com")
        self.assertEqual(page.gen_data_pages(), None)
