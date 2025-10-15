import os
from functools import cached_property

from utils import File, Log

log = Log("AbstractDocTextMixin")


class AbstractDocTextMixin:

    @cached_property
    def text_path(self) -> str:
        return os.path.join(self.dir_doc, "doc.txt")

    @property
    def has_text(self) -> bool:
        return os.path.exists(self.text_path)

    def get_text(self):
        if not self.has_text:
            return None
        return File(self.text_path).read()
