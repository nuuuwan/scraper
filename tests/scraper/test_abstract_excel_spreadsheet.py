import os
import unittest

from scraper import AbstractExcelSpreadsheet


class TestExcelSpreadsheet(AbstractExcelSpreadsheet):
    DIR_TEST = os.path.join(
        "tests", "output", "test_abstract_excel_spreadsheet"
    )

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

    @classmethod
    def get_main_branch_dir_root(cls):
        return os.path.join(cls.DIR_TEST, "data_root")

    @classmethod
    def get_data_branch_dir_root(cls):
        return os.path.join(cls.DIR_TEST, "extended_data_root")


class TestCase(unittest.TestCase):
    def test_init(self):
        doc = TestExcelSpreadsheet.gen_docs().__next__()
        self.assertEqual(doc.num, "1234567890")
        self.assertEqual(doc.url_excel, "http://mock.com/doc.xlsx")

        self.assertEqual(
            doc.excel_path,
            os.path.join(
                doc.get_data_branch_dir_root(),
                "data",
                "scraper",
                "2020s",
                "2023",
                "2023-10-01-1234567890",
                "doc.xlsx",
            ),
        )
