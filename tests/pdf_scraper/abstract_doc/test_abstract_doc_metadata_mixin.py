import os
import shutil
import unittest

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
            doc.get_dir_docs_root(), os.path.join(".", "data", "dummy")
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

    def test_post_write(self):
        DummyDoc.get_dir_root = lambda: os.path.join(
            "tests", "output", "data_parent"
        )
        shutil.rmtree(DummyDoc.get_dir_docs_root(), ignore_errors=True)
        doc = DummyDoc()
        doc.write()
        self.assertTrue(os.path.exists(doc.json_path))

        self.assertEqual(len(DummyDoc.get_all_json_paths()), 1)

        doc2 = DummyDoc.from_file(doc.json_path)
        self.assertEqual(doc2, doc)

        doc_list = DummyDoc.list_all()
        self.assertEqual(len(doc_list), 1)
        self.assertEqual(doc_list[0], doc)

        self.assertEqual(
            DummyDoc.get_url_metadata_set(), {"http://example.com/test.json"}
        )

        self.assertEqual(DummyDoc.year_to_n(), {"2023": 1})
