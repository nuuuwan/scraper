import os
from unittest import TestCase

from scraper import PDFScraperSpider
from tests.test_base_scraper import TEST_URL


class TestPDFScraperSpider(TestCase):
    def test_expanded_pdf_urls(self):
        spider = PDFScraperSpider(TEST_URL)
        self.assertEqual(
            spider.get_expanded_pdf_urls(max_depth=0),
            [
                os.path.join(
                    'https://www.sltda.gov.lk/storage/common_media',
                    'Tourism_Growth_Trends_20211292502899.pdf',
                )
            ],
        )

    def test_expanded_pdf_urls_with_nonzero_max_depth(self):
        spider = PDFScraperSpider(TEST_URL)
        self.assertEqual(
            spider.get_expanded_pdf_urls(max_depth=1),
            [
                os.path.join(
                    'https://www.sltda.gov.lk/storage/common_media',
                    'Tourism_Growth_Trends_20211292502899.pdf',
                )
            ],
        )

    def test_download_all_expanded(self):
        spider = PDFScraperSpider(TEST_URL)
        spider.download_all_expanded()
