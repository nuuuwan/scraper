import os

from utils import File, Log

log = Log("AbstractWorksheetsMixin")


class AbstractWorksheetsMixin:

    @property
    def dir_worksheets(self) -> str:
        return os.path.join(self.dir_doc, "worksheets")

    @property
    def has_worksheets(self) -> bool:
        return os.path.exists(self.dir_worksheets) and bool(
            os.listdir(self.dir_worksheets)
        )

    def extract_worksheets(self) -> None:
        raise NotImplementedError

    # ----------------------------------------------------------------
    # Text (extracted from Worksheet CSVs)
    # ----------------------------------------------------------------

    def extract_text_for_worksheets_mixin(self):
        if os.path.exists(self.text_path):
            return
        if not os.path.exists(self.dir_worksheets):
            return

        content_groups = []
        for file_name in sorted(os.listdir(self.dir_worksheets)):
            if not file_name.endswith(".csv"):
                continue
            csv_path = os.path.join(self.dir_worksheets, file_name)
            content = File(csv_path).read()
            content_groups.append(f"--- {file_name} ---\n")
            content_groups.append(content)

        text = "\n".join(content_groups)
        File(self.text_path).write(text)
        log.info(f"Wrote {self.text_path}")

    def extract_text(self) -> None:
        return self.extract_text_for_worksheets_mixin()

    # ----------------------------------------------------------------
    # Scrape (ALL)
    # ----------------------------------------------------------------
    def scrape_extended_data_for_worksheets_mixin(self):
        if not os.path.exists(self.dir_worksheets):
            self.extract_worksheets()

        if not self.has_text:
            self.extract_text_for_worksheets_mixin()
