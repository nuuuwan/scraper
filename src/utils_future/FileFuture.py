import os
from functools import cached_property

from utils import File


class FileFuture(File):

    def __str__(self):
        return f"{self.path} ({self.size_humanized})"

    def __hash__(self):
        return hash(self.path)

    @cached_property
    def exists(self):
        return os.path.exists(self.path)

    @cached_property
    def size(self):
        return os.path.getsize(self.path)

    @cached_property
    def size_humanized(self):
        size = self.size
        for unit, label in [
            [1_000_000_000, "GB"],
            [1_000_000, "MB"],
            [1_000, "kB"],
        ]:
            if size > unit:
                return f"{size / unit:.1f} {label}"

        return f"{size} B"
