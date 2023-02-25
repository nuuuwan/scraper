from functools import cached_property

from scraper.BaseScraper import BaseScraper, log


class LinkScraper(BaseScraper):
    @cached_property
    def urls(self):
        if self.url.endswith('.pdf'):
            return []

        links = self.soup.find_all('a')
        urls = []
        for link in links:
            url = link.get('href')
            if url and 'http' in url:
                urls.append(url)
        log.debug(f'Extracted {len(urls)} links from {self.url}.')
        return urls
