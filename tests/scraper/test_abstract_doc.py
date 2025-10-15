import os
import random
import unittest
from unittest.mock import patch

from scraper import AbstractDoc

DIR_TEST_ABSTRACT_DOC = os.path.join("tests", "output", "test_abstract_doc")


class DummyDoc(AbstractDoc):
    def __init__(self):
        super().__init__(
            num="1234567890",
            date_str="2023-10-01",
            description="Test Document",
            url_metadata="http://mock.com/doc.html",
            lang="en",
        )

    @classmethod
    def gen_docs(cls):
        yield DummyDoc()

    @classmethod
    def get_main_branch_dir_root(cls):
        return os.path.join(DIR_TEST_ABSTRACT_DOC, "data_root")

    @classmethod
    def get_data_branch_dir_root(cls):
        return os.path.join(DIR_TEST_ABSTRACT_DOC, "extended_data_root")


class TestCase(unittest.TestCase):
    def test_gen_docs(self):
        self.assertEqual(AbstractDoc.gen_docs(), None)

    def test_num_short(self):
        doc = AbstractDoc(
            num="1234567890" * 10,
            date_str="2023-10-01",
            description="Test Document",
            url_metadata="http://mock.com/doc.html",
            lang="en",
        )
        self.assertEqual(doc.num_short, "12345678901234567890123-49cb3608")

    def test_get_dir_root(self):
        self.assertEqual(AbstractDoc.get_main_branch_dir_root(), ".")

    def test_get_data_branch_dir_root(self):
        self.assertEqual(
            AbstractDoc.get_data_branch_dir_root(), "../scraper_data"
        )

    def test_chart(self):
        year_to_lang_to_n = {}
        for year in range(1930, 2026):
            year_to_lang_to_n[year] = {
                "en": random.randint(0, 40),
                "si": random.randint(0, 20),
                "ta": random.randint(0, 10),
            }

        mock_chart_image_path = os.path.join(
            DIR_TEST_ABSTRACT_DOC, "docs_by_year_and_lang.png"
        )
        with patch.object(
            AbstractDoc,
            "get_chart_image_path",
            return_value=mock_chart_image_path,
        ):
            AbstractDoc.build_chart_by_time_and_lang(
                year_to_lang_to_n, "year"
            )
            self.assertTrue(os.path.exists(mock_chart_image_path))

    def test_get_ts(self):
        doc = DummyDoc()
        self.assertEqual(doc.get_ts("decade"), "2020s")
        self.assertEqual(doc.get_ts("year"), "2023")
        self.assertEqual(doc.get_ts("month"), "2023-10")
        self.assertEqual(doc.get_ts("day"), "2023-10-01")
        with self.assertRaises(ValueError):
            doc.get_ts("invalid_time_unit")

    def test_get_best_time_unit(self):
        doc_list = []
        for year in range(2000, 2024):
            for _ in range(random.randint(1, 5)):
                doc = DummyDoc()
                doc.date_str = f"{year}-01-01"
                doc_list.append(doc)

        with patch.object(DummyDoc, "list_all", return_value=doc_list):
            best_time_unit = DummyDoc.get_best_time_unit()
            self.assertEqual(best_time_unit, "year")

    def test_write_all(self):
        doc_list = []
        for year in range(0, 10_000):
            for _ in range(random.randint(1, 5)):
                doc = DummyDoc()
                doc.date_str = f"{year:04d}-01-01"
                doc_list.append(doc)
        os.makedirs(
            os.path.join(
                DummyDoc.get_data_branch_dir_root(), "data", "scraper"
            ),
            exist_ok=True,
        )
        with patch.object(DummyDoc, "list_all", return_value=doc_list):
            DummyDoc.write_all()
