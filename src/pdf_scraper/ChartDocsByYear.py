import os
from functools import cached_property

import matplotlib.pyplot as plt
from utils import Log

log = Log("ChartDocsByYear")


class ChartDocsByYear:
    def __init__(self, doc_class):
        self.doc_class = doc_class

    @cached_property
    def image_path(self) -> str:
        return os.path.join("images", "docs_by_year.png")

    def build(self):
        year_to_n = self.doc_class.year_to_n()
        years = list(year_to_n.keys())
        ns = list(year_to_n.values())

        _, ax = plt.subplots(figsize=(10, 6))
        ax.bar(years, ns)
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of documents")
        ax.set_title(
            f"Number of {self.doc_class.doc_class_label()}"
            + " documents by year"
        )
        ax.set_xticks(years)
        plt.tight_layout()
        os.makedirs(os.path.dirname(self.image_path), exist_ok=True)
        plt.savefig(self.image_path, dpi=300)
        plt.close()
        log.info(f"Wrote {self.image_path}")
