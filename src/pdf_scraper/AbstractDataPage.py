from abc import ABC, abstractmethod
from typing import Generator

from utils_future import WWW

from pdf_scraper.AbstractDoc import AbstractDoc


class AbstractDataPage(WWW, ABC):

    @abstractmethod
    def gen_docs(self) -> Generator[AbstractDoc, None, None]:
        pass
