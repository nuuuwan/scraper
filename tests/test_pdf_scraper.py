import os
from unittest import TestCase

from scraper import PDFScraper
from tests.test_base_scraper import TEST_URL


class TestPDFScraper(TestCase):
    def test_pdf_urls(self):
        scraper = PDFScraper(TEST_URL)
        self.assertEqual(
            scraper.pdf_urls[0],
            os.path.join(
                'https://www.sltda.gov.lk/storage/common_media',
                'Tourism_Growth_Trends_20211292502899.pdf',
            ),
        )

    def test_download_all(self):
        scraper = PDFScraper(TEST_URL)
        scraper.download_all()
