import json
import os
from dataclasses import asdict
from functools import cached_property

from utils import File, Log

from pdf_scraper.hf import HuggingFaceDataset
from pdf_scraper.readme.ChartDocsByYear import ChartDocsByYear
from utils_future import Markdown

log = Log("ReadMe")


class ReadMe:
    N_LATEST = 20

    def __init__(self, home_page_class, doc_class):
        self.home_page_class = home_page_class
        self.doc_class = doc_class
        self.doc_list = self.doc_class.list_all()

    @cached_property
    def readme_path(self) -> str:
        return os.path.join(self.doc_class.get_dir_root(), "README.md")

    @property
    def lines_for_latest_docs(self):
        lines = [f"## {self.N_LATEST} Latest documents", ""]
        for doc in self.doc_list[: self.N_LATEST]:
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

    @property
    def lines_chart_docs_by_year(self) -> list[str]:
        chart = ChartDocsByYear(self.doc_class)
        chart.build()
        return [
            "## Documents By Year",
            "",
            f"![Documents by year]({chart.image_path})",
            "",
        ]

    @property
    def lines_for_metadata_example(self) -> list[str]:
        latest_doc = self.doc_list[0]
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

    @property
    def lines_for_summary(self) -> list[str]:
        n_docs = len(self.doc_list)
        log.debug(f"{n_docs=}")

        n_docs_with_pdfs = len([doc for doc in self.doc_list if doc.has_pdf])

        date_strs = [doc.date_str for doc in self.doc_list]
        date_str_min = min(date_strs)
        date_str_max = max(date_strs)

        url = self.home_page_class().url
        file_size_g = self.doc_class.get_total_file_size() / 1_000_000_000
        log.debug(f"{file_size_g=:.1f}")

        return (
            [
                "## Data Summary",
                "",
            ]
            + Markdown.table(
                [
                    {
                        "Data Source": url,
                        "Date Range": f"{date_str_min} to {date_str_max}",
                        "Number of Docs": f"{n_docs:,}",
                        "Number of Docs with PDFs": f"{n_docs_with_pdfs:,}",
                        "Dataset Size": f"{file_size_g:.1f}GB",
                    },
                ]
            )
            + [""]
        )

    @property
    def lines_for_hugging_face(self):
        lines = ["## 🤗 Hugging Face Datasets", ""]
        hf_dataset = HuggingFaceDataset(self.doc_class)
        for label_suffix in ["docs", "chunks"]:
            dataset_id = hf_dataset.get_dataset_id(label_suffix)
            url = hf_dataset.get_dataset_url(label_suffix)
            lines.append(f"- [{dataset_id}]({url})")
        lines.append("")
        return lines

    @property
    def lines_for_header(self) -> list[str]:
        return [f"# {self.doc_class.doc_class_label().title()}", ""]

    @property
    def lines(self) -> list[str]:
        return (
            self.lines_for_header
            + self.lines_for_summary
            + self.lines_for_metadata_example
            + self.lines_chart_docs_by_year
            + self.lines_for_hugging_face
            + self.lines_for_latest_docs
        )

    def build(self):
        if not self.doc_list:
            log.error("No documents found. Not building README.")
            return
        File(self.readme_path).write("\n".join(self.lines))
        log.info(f"Wrote {self.readme_path}")
