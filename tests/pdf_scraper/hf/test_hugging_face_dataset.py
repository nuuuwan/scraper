import unittest

from pdf_scraper import AbstractDoc, HuggingFaceDataset


class TestCase(unittest.TestCase):
    def test_empty(self):
        hf = HuggingFaceDataset(AbstractDoc)
        self.assertEqual(len(hf.doc_list), 0)
        hf.build_and_upload()
