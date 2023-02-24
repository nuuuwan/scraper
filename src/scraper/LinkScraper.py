from functools import cached_property

from scraper.BaseScraper import BaseScraper, log


class LinkScraper(BaseScraper):
    @cached_property
    def urls(self):
        links = self.soup.find_all('a')
        urls = []
        for link in links:
            urls.append(link.get('href'))
        log.debug(f'Extracted {len(urls)} links from {self.url}.')
        return urls
