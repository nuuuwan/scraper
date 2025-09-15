import sys

from utils import Log

from pdf_scraper.AbstractDoc import AbstractDoc
from pdf_scraper.AbstractHomePage import AbstractHomePage
from pdf_scraper.HuggingFaceDataset import HuggingFaceDataset
from pdf_scraper.PipelineExtendedDataMixin import PipelineExtendedDataMixin
from pdf_scraper.PipelineMetadataMixin import PipelineMetadataMixin
from pdf_scraper.ReadMe import ReadMe

log = Log("Pipeline")


class Pipeline(PipelineMetadataMixin, PipelineExtendedDataMixin):
    class DEFAULT:
        MAX_DT = 750

    def __init__(
        self,
        home_page_class: type[AbstractHomePage],
        doc_class: type[AbstractDoc],
    ):
        self.home_page_class = home_page_class
        self.doc_class = doc_class

    def run(self):
        max_dt = int(sys.argv[1]) if len(sys.argv) > 1 else None
        max_dt = max_dt or Pipeline.DEFAULT.MAX_DT
        log.debug(f"{max_dt=}s")
        self.__scrape_metadata__(max_dt)
        self.__scrape_extended_data__(max_dt)
        ReadMe(self.home_page_class, self.doc_class).build()
        HuggingFaceDataset(self.doc_class).build_and_upload()
