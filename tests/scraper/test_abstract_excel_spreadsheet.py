import unittest

from scraper import AbstractExcelSpreadsheet


class TestCase(unittest.TestCase):
    def test_init(self):
        doc = AbstractExcelSpreadsheet(
            num="1234567890",
            date_str="2023-10-01",
            description="Test Document",
            url_metadata="http://mock.com/doc.html",
            lang="en",
            url_excel="http://mock.com/doc.xlsx",
        )
        self.assertEqual(doc.num, "1234567890")
        self.assertEqual(doc.url_excel, "http://mock.com/doc.xlsx")
