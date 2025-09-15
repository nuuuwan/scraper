import unittest

from pdf_scraper import AbstractDataPage


class TestCase(unittest.TestCase):
    def test_method(self):
        page = AbstractDataPage(url="http://example.com")
        self.assertEqual(page.gen_docs(), None)
