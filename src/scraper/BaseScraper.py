from functools import cached_property

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import File, Log, hashx

log = Log('Scraper')


class BaseScraper:
    def __init__(self, url):
        self.url = url

    @cached_property
    def hash(self):
        return hashx.md5(self.url)

    @cached_property
    def local_html_path(self):
        return f'/tmp/scraper.{self.hash}.htm'

    @cached_property
    def local_html_file(self):
        return File(self.local_html_path)

    @cached_property
    def html(self):
        if self.local_html_file.exists:
            return self.local_html_file.read()

        log.debug(f'Scraping {self.url}...')
        # scrapes html using selenium
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(self.url)
        html = driver.page_source
        driver.close()
        driver.quit()
        html_size = len(html)
        log.debug(
            f'Scraped {self.url} to {self.local_html_path} ({html_size:,}B)'
        )
        self.local_html_file.write(html)
        return html

    @property
    def soup(self):
        return BeautifulSoup(self.html, 'html.parser')
