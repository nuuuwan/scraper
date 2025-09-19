import os
import shutil
import unittest
from unittest.mock import patch

from utils import JSONFile

from scraper import AbstractDoc, ReadMe


class TestCase(unittest.TestCase):
    def test_build(self):
        mock_data_branch_dir_root_data = os.path.join(
            "tests", "output", "test_readme", "data_branch", "data"
        )
        if os.path.exists(mock_data_branch_dir_root_data):
            shutil.rmtree(mock_data_branch_dir_root_data)
        os.makedirs(mock_data_branch_dir_root_data, exist_ok=True)

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
                    doc_class_description="This is a mock doc class for testing",
                    time_updated="2024-01-01 12:00:00",
                    n_docs=10,
                    n_docs_with_pdfs=5,
                    n_docs_with_text=3,
                    date_str_min="2023-01-01",
                    date_str_max="2023-12-31",
                    dataset_size=123_456_789,
                    url_source="https://example.com/mock_doc_class",
                    url_data="https://example.com/mock_doc_class/data",
                    latest_doc_d=dict(
                        lang="si-en",
                    ),
                )
            )

        mock_main_branch_dir_root = os.path.join(
            "tests", "output", "test_readme", "main_branch"
        )
        if os.path.exists(mock_main_branch_dir_root):
            shutil.rmtree(mock_main_branch_dir_root)
        os.makedirs(mock_main_branch_dir_root, exist_ok=True)
        mock_readme_path = os.path.join(mock_main_branch_dir_root, "README.md")
        with patch.object(
            ReadMe,
            "PATH",
            new=mock_readme_path,
        ), patch.object(
            AbstractDoc,
            "get_data_branch_dir_root_data",
            return_value=mock_data_branch_dir_root_data,
        ):
            self.assertEqual(
                AbstractDoc.get_data_branch_dir_root_data(),
                mock_data_branch_dir_root_data,
            )
            self.assertEqual(ReadMe.PATH, mock_readme_path)
            ReadMe.build()
            self.assertTrue(os.path.exists(mock_readme_path))
