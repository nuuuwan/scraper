from pdf_scraper.abstract_doc.AbstractDocBase import AbstractDocBase
from pdf_scraper.abstract_doc.AbstractDocExtendedDataMixin import \
    AbstractDocExtendedDataMixin
from pdf_scraper.abstract_doc.AbstractDocGeneratorMixin import \
    AbstractDocGeneratorMixin
from pdf_scraper.abstract_doc.AbstractDocHuggingFaceMixin import \
    AbstractDocHuggingFaceMixin
from pdf_scraper.abstract_doc.AbstractDocMetadataMixin import \
    AbstractDocMetadataMixin
from pdf_scraper.abstract_doc.AbstractDocReadMeMixin import \
    AbstractDocReadMeMixin
from pdf_scraper.abstract_doc.pipeline.AbstractDocPipelineMixin import \
    AbstractDocPipelineMixin


class AbstractDoc(
    AbstractDocBase,
    AbstractDocGeneratorMixin,
    AbstractDocMetadataMixin,
    AbstractDocExtendedDataMixin,
    AbstractDocReadMeMixin,
    AbstractDocHuggingFaceMixin,
    AbstractDocPipelineMixin,
):
    pass
