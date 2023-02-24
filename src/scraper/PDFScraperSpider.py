from utils import Log

from scraper.PDFScraper import PDFScraper

log = Log('PDFScraperSpider')


class PDFScraperSpider(PDFScraper):
    def get_expanded_pdf_urls(self, max_depth=0):
        pdf_urls = self.pdf_urls
        if max_depth > 0:
            for url in self.urls:
                if 'http' not in url:
                    log.error(f'Not spidering {url}.')
                    continue
                if url.endswith('.pdf'):
                    log.debug(f'Not spidering PDF {url}.')
                    continue
                scraper = PDFScraperSpider(url)
                pdf_urls += scraper.get_expanded_pdf_urls(max_depth - 1)

        log.debug(f'Found {len(pdf_urls)} PDF URLs in {self.url}.')
        return pdf_urls

    def download_all_expanded(self, max_depth=0):
        return PDFScraper.download_all_helper(
            self.get_expanded_pdf_urls(max_depth=max_depth)
        )
