import os
import shutil
import unittest

from pdf_scraper import AbstractDoc


class TestDoc(AbstractDoc):
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
        test_doc = TestDoc()
        self.assertEqual(
            test_doc.dir_doc,
            os.path.join(
                "data", "test", "2020s", "2023", "2023-10-01-1234567890"
            ),
        )
        self.assertEqual(
            test_doc.json_path,
            os.path.join(
                test_doc.dir_doc,
                "doc.json",
            ),
        )

    def test_post_write(self):
        TestDoc.get_dir_docs_root = lambda: os.path.join(
            "tests", "output", "data"
        )
        shutil.rmtree(TestDoc.get_dir_docs_root(), ignore_errors=True)
        test_doc = TestDoc()
        test_doc.write()
        self.assertTrue(os.path.exists(test_doc.json_path))

        self.assertEqual(len(TestDoc.get_all_json_paths()), 1)

        test_doc2 = TestDoc.from_file(test_doc.json_path)
        self.assertEqual(test_doc2, test_doc)

        doc_list = TestDoc.list_all()
        self.assertEqual(len(doc_list), 1)
        self.assertEqual(doc_list[0], test_doc)

        self.assertEqual(
            TestDoc.get_url_metadata_set(), {"http://example.com/test.json"}
        )

        self.assertEqual(TestDoc.year_to_n(), {"2023": 1})
