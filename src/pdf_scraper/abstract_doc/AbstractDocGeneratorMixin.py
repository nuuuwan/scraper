from abc import ABC
from typing import Generator

from pdf_scraper.abstract_doc import AbstractDoc


class AbstractDocGeneratorMixin(ABC):
    @classmethod
    def gen_docs(cls) -> Generator[AbstractDoc, None, None]:
        pass
