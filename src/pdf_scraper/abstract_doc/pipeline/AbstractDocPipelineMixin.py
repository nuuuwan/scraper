import sys

from utils import Log

from pdf_scraper.abstract_doc.pipeline.AbstractDocPipelineCleanupMixin import \
    AbstractDocPipelineCleanupMixin
from pdf_scraper.abstract_doc.pipeline.AbstractDocPipelineExtendedDataMixin import \
    AbstractDocPipelineExtendedDataMixin
from pdf_scraper.abstract_doc.pipeline.AbstractDocPipelineMetadataMixin import \
    AbstractDocPipelineMetadataMixin

log = Log("AbstractDocPipelineMixin")


class AbstractDocPipelineMixin(
    AbstractDocPipelineMetadataMixin,
    AbstractDocPipelineExtendedDataMixin,
    AbstractDocPipelineCleanupMixin,
):
    MAX_DT = 750.0

    @classmethod
    def run_pipeline(cls, max_dt=None):
        max_dt = (
            max_dt
            or (float(sys.argv[1]) if len(sys.argv) > 1 else None)
            or AbstractDocPipelineMixin.MAX_DT
        )
        log.debug(f"{max_dt=}s")
        cls.cleanup()
        cls.scrape_metadata(max_dt)
        cls.scrape_extended_data(max_dt)
        cls.readme_build()
        cls.build_and_upload()
