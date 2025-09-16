import unittest

from pdf_scraper import AbstractDocGenerator


class TestCase(unittest.TestCase):
    def test_method(self):
        page = AbstractDocGenerator()
        self.assertEqual(page.gen_docs(), None)
