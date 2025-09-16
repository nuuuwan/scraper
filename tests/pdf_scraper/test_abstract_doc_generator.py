import unittest

from pdf_scraper import AbstractDoc


class TestCase(unittest.TestCase):
    def test_method(self):
        self.assertEqual(AbstractDoc.gen_docs(), None)
