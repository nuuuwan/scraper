import os
import shutil
import unittest
from unittest.mock import patch

from utils_future import BigJSONFile


class TestCase(unittest.TestCase):
    def test_read_and_write(self):
        with patch(
            "utils_future.BigJSONFile.BigJSONFile.MIN_BIG_FILE_SIZE",
            1_000,
        ):
            self.assertTrue(BigJSONFile.MIN_BIG_FILE_SIZE, 1_000)
            data_list = [f"{i:08d}" for i in range(1_000)]
            big_json_file = BigJSONFile(
                os.path.join("tests", "output", "test_big_json_file")
            )
            big_json_file.write(data_list)
            data_list2 = big_json_file.read()
            self.assertEqual(data_list, data_list2)

    def test_empty(self):
        dir_path = os.path.join("tests", "output", "test_big_json_file_empty")
        shutil.rmtree(dir_path, ignore_errors=True)
        big_json_file = BigJSONFile(dir_path)
        data_list = big_json_file.read()
        self.assertEqual(data_list, [])
        big_json_file.write([])
        data_list2 = big_json_file.read()
        self.assertEqual(data_list2, [])
        shutil.rmtree(dir_path, ignore_errors=True)
