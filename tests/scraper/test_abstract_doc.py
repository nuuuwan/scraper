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
                "en": random.randint(0, 20),
                "si": random.randint(0, 20),
                "ta": random.randint(0, 20),
            }

        mock_chart_image_path = os.path.join(
            DIR_TEST_ABSTRACT_DOC, "docs_by_year_and_lang.png"
        )
        with patch.object(
            AbstractDoc,
            "get_chart_image_path",
            return_value=mock_chart_image_path,
        ):
            AbstractDoc.build_chart_by_year_and_lang(year_to_lang_to_n)
            self.assertTrue(os.path.exists(mock_chart_image_path))
