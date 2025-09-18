from scraper.abstract_doc.AbstractDocBase import AbstractDocBase
from scraper.abstract_doc.AbstractDocExtendedDataMixin import \
    AbstractDocExtendedDataMixin
from scraper.abstract_doc.AbstractDocGeneratorMixin import \
    AbstractDocGeneratorMixin
from scraper.abstract_doc.AbstractDocHuggingFaceMixin import \
    AbstractDocHuggingFaceMixin
from scraper.abstract_doc.AbstractDocMetadataMixin import \
    AbstractDocMetadataMixin
from scraper.abstract_doc.AbstractDocReadMeMixin import AbstractDocReadMeMixin
from scraper.abstract_doc.pipeline.AbstractDocPipelineMixin import \
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
