import os
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
    def local_path(self):
        ext = self.url.split('.')[-1]
        if len(ext) > 4:
            ext = 'htm'
        return f'/tmp/scraper.{self.hash}.{ext}'

    @cached_property
    def local_file(self):
        return File(self.local_path)

    @cached_property
    def html(self):
        if self.local_file.exists:
            return self.local_file.read()

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
        log.debug(f'Scraped {self.url} to {self.local_path} ({html_size:,}B)')
        self.local_file.write(html)
        return html

    @property
    def soup(self):
        return BeautifulSoup(self.html, 'html.parser')

    def download_binary(self):
        if self.local_file.exists:
            log.debug(f'{self.local_path} already exists.')
            return self.local_file.path

        os.system(f'wget -O {self.local_path} {self.url}')
        file_size = os.path.getsize(self.local_path)
        log.debug(
            f'Downloaded {self.url} to {self.local_path} ({file_size:,}B)'
        )
        return self.local_file.path
