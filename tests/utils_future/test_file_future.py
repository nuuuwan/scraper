import os
import unittest

from utils_future import FileOrDirFuture


class TestCase(unittest.TestCase):
    def test_method(self):
        file_path = os.path.join("tests", "output", "test.txt")
        f = FileOrDirFuture(file_path)
        content = "12345678" * 1_000
        f.write(content)
        self.assertTrue(f.exists)
        self.assertEqual(hash(f), hash(file_path))
        self.assertEqual(f.size, len(content))
        self.assertEqual(f.size_humanized, "8.0 kB")
        self.assertEqual(str(f), f"{file_path} (8.0 kB)")

    def test_small_file(self):
        file_path = os.path.join("tests", "output", "test_small.txt")
        f = FileOrDirFuture(file_path)
        content = "12345678"
        f.write(content)
        self.assertEqual(str(f), f"{file_path} (8 B)")

    def test_dir(self):
        dir_path = os.path.join("tests", "input")
        d = FileOrDirFuture(dir_path)
        self.assertTrue(d.exists)
        self.assertEqual(d.size, 231_412)
        self.assertEqual(d.size_humanized, "231.4 kB")
