import json
import os

from utils import File, Log, Time, TimeFormat

from scraper.abstract_doc.readme.AbstractDocChartDocsByYearMixin import \
    AbstractDocChartDocsByYearMixin

log = Log("AbstractDocReadMeMixin")


class AbstractDocReadMeMixin(AbstractDocChartDocsByYearMixin):
    N_LATEST = 20

    @classmethod
    def get_dir_root(cls) -> str:
        return "."

    @classmethod
    def get_readme_path(cls) -> str:
        return os.path.join(cls.get_dir_root(), "README.md")

    @classmethod
    def get_lines_for_latest_docs(cls):
        lines = [f"## 🆕 {cls.N_LATEST} Latest documents", ""]
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
            "## 📝 Example Metadata",
            "",
            "```json",
            json.dumps(latest_doc.to_dict(), indent=4),
            "```",
            "",
        ]

    @classmethod
    def get_lines_for_summary(cls) -> list[str]:
        n_docs = len(cls.list_all())
        n_docs_with_pdfs = len([doc for doc in cls.list_all() if doc.has_pdf])
        p_docs_with_pdfs = n_docs_with_pdfs / n_docs
        date_strs = [doc.date_str for doc in cls.list_all()]
        date_str_min = min(date_strs)
        date_str_max = max(date_strs)
        file_size_g = cls.get_total_file_size() / 1_000_000_000
        latest_doc = cls.list_all()[0]
        url_source = latest_doc.url_metadata.split("?")[0]
        url_data = cls.get_remote_data_url_base()
        url_repo = cls.get_remote_repo_url()

        lines = [
            f"📜 [**{n_docs:,}** documents]({url_data})"
            + f" (**{file_size_g:.1f} GB**),"
            + f" from **{date_str_min}** to **{date_str_max}**,"
            + f" scraped from **[{url_source}]({url_source})**",
            "",
            "📑 In JSON, PDF, TXT and 🤗 Hugging Face Formats",
            "",
            "⏰ Updated **at least Daily**",
            "",
            "🆓 Public data & fully open-source",
            "",
            "#OpenData #DataScience #DataForGood #ResearchData #NLP",
            "",
            "...",
            "",
            "*📒 PDFs have been downloaded for"
            + f" **{n_docs_with_pdfs:,}**"
            + f" (**{p_docs_with_pdfs:.0%}**) documents*",
            "",
            "🪲 #WorkInProgress - Suggestions, Questions, Ideas,"
            + f" & [Bug Reports]({url_repo}/issues)"
            + " are welcome!",
            "",
        ]
        return lines

    @classmethod
    def get_lines_for_hugging_face(cls):
        url_hf = (
            "https://img.shields.io/badge"
            + "/-HuggingFace-FDEE21"
            + "?style=for-the-badge&logo=HuggingFace"
        )
        lines = [
            "## 🤗 Hugging Face Datasets",
            "",
            f"![HuggingFace]({url_hf})",
            "",
        ]

        for emoji, label_suffix in [["📄", "docs"], ["📦", "chunks"]]:
            dataset_id = cls.get_dataset_id(label_suffix)
            url = cls.get_dataset_url(label_suffix)
            lines.append(f"- {emoji} [{dataset_id}]({url})")
        lines.append("")
        return lines

    @classmethod
    def get_title(cls) -> str:
        title = cls.get_doc_class_label().title().replace("_", " ")
        title = title.replace("Lk", "🇱🇰 #SriLanka")
        return title

    @classmethod
    def get_lines_for_header(cls) -> list[str]:
        time_updated = TimeFormat("%Y--%m--%d_%H:%M:%S").format(Time.now())
        file_size_g = cls.get_total_file_size() / 1_000_000_000
        url_repo = cls.get_remote_repo_url()
        return [
            f"# {cls.get_title()} `Dataset`",
            "",
            "![LastUpdated](https://img.shields.io/badge"
            + f"/last_updated-{time_updated}-green)",
            "![DatasetSize](https://img.shields.io/badge"
            + f"/dataset_size-{file_size_g:.1f}_GB-yellow)",
            "",
            f"[{url_repo}]({url_repo})",
            "",
        ]

    @classmethod
    def get_lines_for_footer(cls) -> list[str]:
        return [
            "---",
            "",
            "![Maintainer](https://img.shields.io/badge"
            + "/maintainer-nuuuwan-red)",
            "![MadeWith](https://img.shields.io/badge/made_with-python-blue)",
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
            + cls.get_lines_for_footer()
        )

    @classmethod
    def build_readme(cls):
        assert cls.list_all()
        os.makedirs(cls.get_dir_root(), exist_ok=True)
        readme_path = cls.get_readme_path()
        File(readme_path).write("\n".join(cls.lines()))
        log.info(f"Wrote {readme_path}")
