import unittest

from scraper import AbstractExcelSpreadsheet


class TestExcelSpreadsheet(AbstractExcelSpreadsheet):

    @classmethod
    def gen_docs(cls):
        yield TestExcelSpreadsheet(
            num="1234567890",
            date_str="2023-10-01",
            description="Test Document",
            url_metadata="http://mock.com/doc.html",
            lang="en",
            url_excel="http://mock.com/doc.xlsx",
        )


class TestCase(unittest.TestCase):
    def test_init(self):
        doc = TestExcelSpreadsheet.gen_docs().__next__()
        self.assertEqual(doc.num, "1234567890")
        self.assertEqual(doc.url_excel, "http://mock.com/doc.xlsx")
