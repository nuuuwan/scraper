from abc import ABC
from typing import Generator

from pdf_scraper.pages.AbstractDataPage import AbstractDataPage
from utils_future import WWW


class AbstractHomePage(WWW, ABC):

    def gen_data_pages(self) -> Generator[AbstractDataPage, None, None]:
        pass
