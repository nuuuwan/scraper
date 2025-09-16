import json
import os
from dataclasses import asdict
from urllib.parse import urlparse

from utils import File, Log

from pdf_scraper.abstract_doc.AbstractDocChartDocsByYearMixin import \
    AbstractDocChartDocsByYearMixin
from utils_future import Markdown

log = Log("AbstractDocReadMeMixin")


class AbstractDocReadMeMixin(AbstractDocChartDocsByYearMixin):
    N_LATEST = 20

    @classmethod
    def get_readme_path(cls) -> str:
        return os.path.join(cls.get_dir_root(), "README.md")

    @classmethod
    def get_lines_for_latest_docs(cls):
        lines = [f"## {cls.N_LATEST} Latest documents", ""]
        for doc in cls.list_all()[: cls.N_LATEST]:
            line = "- " + " | ".join(
                [
                    doc.date_str,
                    f"`{doc.num}`",
                    doc.description,
                    f"[data]({doc.remote_data_url})",
                ]
            )
            lines.append(line)
        lines.append("")
        return lines

    @classmethod
    def get_lines_chart_docs_by_year(cls) -> list[str]:
        cls.get_chart_build()
        return [
            "## Documents By Year",
            "",
            f"![Documents by year]({cls.get_chart_image_path()})",
            "",
        ]

    @classmethod
    def get_lines_for_metadata_example(cls) -> list[str]:
        latest_doc = cls.list_all()[0]
        return [
            "## Document Metadata Example",
            "",
            "```json",
            json.dumps(asdict(latest_doc), indent=4),
            "```",
            "",
            f"[source data]({latest_doc.remote_data_url})",
            "",
        ]

    @classmethod
    def get_lines_for_summary(cls) -> list[str]:
        n_docs = len(cls.list_all())
        log.debug(f"{n_docs=}")

        n_docs_with_pdfs = len([doc for doc in cls.list_all() if doc.has_pdf])

        date_strs = [doc.date_str for doc in cls.list_all()]
        date_str_min = min(date_strs)
        date_str_max = max(date_strs)

        file_size_g = cls.get_total_file_size() / 1_000_000_000
        log.debug(f"{file_size_g=:.1f}")

        latest_doc = cls.list_all()[0]
        netloc = urlparse(latest_doc.url_metadata).netloc

        return (
            [
                "## Data Summary",
                "",
            ]
            + Markdown.table(
                [
                    {
                        "Data Source": netloc,
                        "Date Range": f"{date_str_min} to {date_str_max}",
                        "Number of Docs": f"{n_docs:,}",
                        "Number of Docs with PDFs": f"{n_docs_with_pdfs:,}",
                        "Dataset Size": f"{file_size_g:.1f}GB",
                    },
                ]
            )
            + [""]
        )

    @classmethod
    def get_lines_for_hugging_face(cls):
        lines = ["## 🤗 Hugging Face Datasets", ""]

        for label_suffix in ["docs", "chunks"]:
            dataset_id = cls.get_dataset_id(label_suffix)
            url = cls.get_dataset_url(label_suffix)
            lines.append(f"- [{dataset_id}]({url})")
        lines.append("")
        return lines

    @classmethod
    def get_lines_for_header(cls) -> list[str]:
        return [
            f"# {cls.get_doc_class_label().title()}",
            "",
            cls.get_doc_class_description(),
            "",
        ]

    @classmethod
    def lines(cls) -> list[str]:
        return (
            cls.get_lines_for_header()
            + cls.get_lines_for_summary()
            + cls.get_lines_for_metadata_example()
            + cls.get_lines_chart_docs_by_year()
            + cls.get_lines_for_hugging_face()
            + cls.get_lines_for_latest_docs()
        )

    @classmethod
    def build_readme(cls):
        assert cls.list_all()
        readme_path = cls.get_readme_path()
        File(readme_path).write("\n".join(cls.lines()))
        log.info(f"Wrote {readme_path}")
