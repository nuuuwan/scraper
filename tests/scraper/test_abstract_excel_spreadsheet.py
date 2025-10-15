import os
import shutil
import unittest

from utils import File

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
            url_excel="https://github.com/nuuuwan"
            + "/scraper/raw/refs/heads/main/tests/input/test.xlsx",
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

        shutil.rmtree(doc.get_data_branch_dir_root(), ignore_errors=True)
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
        self.assertFalse(doc.has_excel)

    def test_write(self):
        doc = TestExcelSpreadsheet.gen_docs().__next__()
        shutil.rmtree(doc.get_data_branch_dir_root(), ignore_errors=True)
        doc.write()
        doc.extract_text()
        doc.extract_tabular()
        doc.download_excel()
        doc.download_excel()
        self.assertTrue(doc.has_excel)
        doc.extract_tabular()
        doc.extract_tabular()
        self.assertTrue(doc.has_tabular)
        File(os.path.join(doc.dir_tabular, "fake.fake")).write("fake")
        doc.extract_text()
        doc.extract_text()
        self.assertTrue(doc.has_text)

    def test_scrape_extended_data_for_doc(self):
        doc = TestExcelSpreadsheet.gen_docs().__next__()
        shutil.rmtree(doc.get_data_branch_dir_root(), ignore_errors=True)
        doc.write()
        self.assertFalse(doc.has_excel)
        self.assertFalse(doc.has_tabular)
        self.assertFalse(doc.has_text)
        doc.scrape_extended_data_for_doc()
        self.assertTrue(doc.has_excel)
        self.assertTrue(doc.has_tabular)
        self.assertTrue(doc.has_text)
        doc.scrape_extended_data_for_doc()

    def test_open_excel(self):
        for excel_file_name in [
            "test.xlsx",
            "test-old.xls",
            "test-old-fisheries.xls",
        ]:
            excel_path = os.path.join("tests", "input", excel_file_name)
            excel = TestExcelSpreadsheet.open_excel(excel_path)
            self.assertIsNotNone(excel)
