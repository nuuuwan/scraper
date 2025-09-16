import sys

from utils import Log

from pdf_scraper.abstract_doc import AbstractDoc
from pdf_scraper.hf import HuggingFaceDataset
from pdf_scraper.pages import AbstractHomePage
from pdf_scraper.pipeline.PipelineCleanupMixin import PipelineCleanupMixin
from pdf_scraper.pipeline.PipelineExtendedDataMixin import \
    PipelineExtendedDataMixin
from pdf_scraper.pipeline.PipelineMetadataMixin import PipelineMetadataMixin
from pdf_scraper.readme import ReadMe

log = Log("Pipeline")


class Pipeline(
    PipelineMetadataMixin, PipelineExtendedDataMixin, PipelineCleanupMixin
):
    class DEFAULT:
        MAX_DT = 750.0

    def __init__(
        self,
        home_page_class: type[AbstractHomePage],
        doc_class: type[AbstractDoc],
    ):
        self.home_page_class = home_page_class
        self.doc_class = doc_class

    def run(self, max_dt=None):
        max_dt = (
            max_dt
            or (float(sys.argv[1]) if len(sys.argv) > 1 else None)
            or Pipeline.DEFAULT.MAX_DT
        )
        log.debug(f"{max_dt=}s")
        self.cleanup()
        self.scrape_metadata(max_dt)
        self.scrape_extended_data(max_dt)
        ReadMe(self.home_page_class, self.doc_class).build()
        HuggingFaceDataset(self.doc_class).build_and_upload()
