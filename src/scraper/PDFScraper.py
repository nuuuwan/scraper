from functools import cached_property

from scraper.BaseScraper import BaseScraper, log
from scraper.LinkScraper import LinkScraper


class PDFScraper(LinkScraper):
    @cached_property
    def pdf_urls(self):
        return [url for url in self.urls if url.endswith('.pdf')]

    def download_all(self):
        pdf_file_paths = []
        for url in self.pdf_urls:
            scraper = BaseScraper(url)
            pdf_file_paths.append(scraper.download_binary())
        log.info(f'Downloaded {len(pdf_file_paths)} PDF files')
        return pdf_file_paths
