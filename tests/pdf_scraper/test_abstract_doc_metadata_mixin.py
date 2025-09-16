import os
import shutil
import unittest
from unittest.mock import patch

from pdf_scraper import AbstractDoc


class DummyDoc(AbstractDoc):
    def __init__(self):
        super().__init__(
            num="1234567890",
            date_str="2023-10-01",
            description="Test Document",
            url_pdf="http://example.com/test.pdf",
            url_metadata="http://example.com/test.json",
        )


class TestCase(unittest.TestCase):
    def test_base(self):
        doc = DummyDoc()

        self.assertEqual(
            doc.get_dir_docs_for_cls(), os.path.join(".", "data", "dummy")
        )
        self.assertEqual(
            doc.dir_doc,
            os.path.join(
                ".", "data", "dummy", "2020s", "2023", "2023-10-01-1234567890"
            ),
        )
        self.assertEqual(
            doc.json_path,
            os.path.join(
                doc.dir_doc,
                "doc.json",
            ),
        )
        self.assertTrue(not os.path.exists("data"))

    def test_post_write(self):
        mock_dir_root = os.path.join("tests", "output", "data_parent")
        shutil.rmtree(mock_dir_root, ignore_errors=True)

        with patch.object(
            DummyDoc, "get_dir_root", return_value=mock_dir_root
        ):

            doc = DummyDoc()
            self.assertEqual(
                doc.get_dir_root(),
                mock_dir_root,
            )
            self.assertEqual(
                doc.json_path,
                os.path.join(
                    mock_dir_root,
                    "data",
                    "dummy",
                    "2020s",
                    "2023",
                    "2023-10-01-1234567890",
                    "doc.json",
                ),
            )
            doc.write()
            self.assertTrue(os.path.exists(doc.json_path))

            self.assertEqual(len(DummyDoc.get_all_json_paths()), 1)
            doc2 = DummyDoc.from_file(doc.json_path)
            self.assertEqual(doc2, doc)

            doc_list = DummyDoc.list_all()
            self.assertEqual(len(doc_list), 1)
            self.assertEqual(doc_list[0], doc)

            self.assertEqual(
                DummyDoc.get_url_metadata_set(),
                {"http://example.com/test.json"},
            )
            self.assertEqual(DummyDoc.year_to_n(), {"2023": 1})

        self.assertTrue(not os.path.exists("data"))
