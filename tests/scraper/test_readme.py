import os
import shutil
import unittest
from unittest.mock import patch

from scraper import AbstractDoc, ReadMe


class TestCase(unittest.TestCase):
    def test_build(self):
        mock_data_branch_dir_root_data = os.path.join(
            "tests", "output", "test_readme", "data_branch", "data"
        )
        if os.path.exists(mock_data_branch_dir_root_data):
            shutil.rmtree(mock_data_branch_dir_root_data)
        os.makedirs(mock_data_branch_dir_root_data, exist_ok=True)

        with patch.object(
            ReadMe,
            "PATH",
            return_value=os.path.join(
                "tests", "output", "test_readme", "main_branch", "README.md"
            ),
        ), patch.object(
            AbstractDoc,
            "get_data_branch_dir_root_data",
            return_value=mock_data_branch_dir_root_data,
        ):
            self.assertEqual(
                AbstractDoc.get_data_branch_dir_root_data(),
                mock_data_branch_dir_root_data,
            )
            ReadMe.build()
