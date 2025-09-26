import os
import shutil
import unittest
from unittest.mock import patch

from utils import JSONFile

from scraper import AbstractDoc


class TestCase(unittest.TestCase):
    @staticmethod
    def __build_mock_data__(mock_data_branch_dir_root_data):
        for i in range(10):
            mock_doc_class_dir = os.path.join(
                mock_data_branch_dir_root_data, f"mock_doc_class-{i}"
            )
            os.makedirs(mock_doc_class_dir, exist_ok=True)
            mock_summary_path = os.path.join(
                mock_doc_class_dir, "summary.json"
            )
            JSONFile(mock_summary_path).write(
                dict(
                    doc_class_label=f"mock_doc_class-{i}",
                    doc_class_description="This is a mock doc for testing",
                    doc_class_emoji="🇱🇰",
                    time_updated="2024-01-01 12:00:00",
                    n_docs=10,
                    n_docs_with_pdfs=5,
                    n_docs_with_text=3,
                    date_str_min="2023-01-01",
                    date_str_max="2023-12-31",
                    dataset_size=123_456_789,
                    url_source_list=["https://example.com/mock_doc_class"],
                    url_data="https://example.com/mock_doc_class/data",
                    latest_doc_d=dict(),
                    langs=["si-en", "ta", "en"],
                    year_to_lang_to_n={
                        2020: {"en": 5, "si": 3},
                        2021: {"en": 10, "si": 7, "ta": 2},
                    },
                    url_chart="https://example.com/mock_doc_class/chart.png",
                )
            )

    def test_build(self):
        mock_data_branch_dir_root_data = os.path.join(
            "tests", "output", "test_readme", "data_branch", "data"
        )
        if os.path.exists(mock_data_branch_dir_root_data):
            shutil.rmtree(mock_data_branch_dir_root_data)
        os.makedirs(mock_data_branch_dir_root_data, exist_ok=True)

        self.__class__.__build_mock_data__(mock_data_branch_dir_root_data)

        mock_main_branch_dir_root = os.path.join(
            "tests", "output", "test_readme", "main_branch"
        )
        if os.path.exists(mock_main_branch_dir_root):
            shutil.rmtree(mock_main_branch_dir_root)
        os.makedirs(mock_main_branch_dir_root, exist_ok=True)

        with patch.object(
            AbstractDoc,
            "get_data_branch_dir_root_data",
            return_value=mock_data_branch_dir_root_data,
        ):
            self.assertEqual(
                AbstractDoc.get_data_branch_dir_root_data(),
                mock_data_branch_dir_root_data,
            )
