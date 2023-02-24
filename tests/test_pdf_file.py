from unittest import TestCase

from scraper import PDFFile

TEST_PDF_FILE = PDFFile('tests/example.pdf')


class TestPDFFile(TestCase):
    def test_dir_tables(self):
        self.assertEqual(
            TEST_PDF_FILE.dir_tables.path, 'tests/example.pdf.tables'
        )

    def test_tables(self):
        self.assertEqual(
            TEST_PDF_FILE.tables,
            [
                'tests/example.pdf.tables/table-00.tsv',
            ],
        )
