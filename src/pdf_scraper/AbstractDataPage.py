from abc import ABC, abstractmethod
from typing import Generator

from pdf_scraper.AbstractDoc import AbstractDoc
from utils_future import WWW


class AbstractDataPage(WWW, ABC):

    @abstractmethod
    def gen_docs(self) -> Generator[AbstractDoc, None, None]:
        pass
