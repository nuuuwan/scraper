from utils import Log

from utils_future.FileFuture import FileFuture
from utils_future.pdf_file.PDFTextMixin import PDFTextMixin

log = Log("PDFFile")


class PDFFile(FileFuture, PDFTextMixin):

    def __init__(self, path):
        assert path.endswith(".pdf")
        super().__init__(path)
