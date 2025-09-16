import os

import matplotlib.pyplot as plt
from utils import Log

log = Log("AbstractDocChartDocsByYearMixin")


class AbstractDocChartDocsByYearMixin:

    @classmethod
    def image_path(cls) -> str:
        return os.path.join("images", "docs_by_year.png")

    @classmethod
    def build(cls):
        year_to_n = cls.year_to_n()
        years = list(year_to_n.keys())
        ns = list(year_to_n.values())

        _, ax = plt.subplots(figsize=(10, 6))
        ax.bar(years, ns)
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of documents")
        ax.set_title(
            f"Number of {cls.doc_class_label()}" + " documents by year"
        )
        ax.set_xticks(years)
        plt.tight_layout()
        os.makedirs(os.path.dirname(cls.image_path), exist_ok=True)
        plt.savefig(cls.image_path, dpi=300)
        plt.close()
        log.info(f"Wrote {cls.image_path}")
