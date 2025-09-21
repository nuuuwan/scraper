import os
import time
from typing import Generator

from utils import Log

log = Log("AbstractDocPipelineExtendedDataMixin")


class AbstractDocPipelineExtendedDataMixin:
    EXTENDED_PROCESSING_BATCHS_SIZE = 8

    @classmethod
    def gen_doc_batch_list(cls) -> Generator[list, None, None]:
        all_docs = cls.list_all()
        for i in range(0, len(all_docs), cls.EXTENDED_PROCESSING_BATCHS_SIZE):
            i_start = i
            i_end = min(
                i + cls.EXTENDED_PROCESSING_BATCHS_SIZE, len(all_docs)
            )
            yield all_docs[i_start:i_end]

    @classmethod
    def process_doc_batch(cls, doc_batch):
        for doc in doc_batch:
            try:
                doc.scrape_extended_data_for_doc()
            except Exception as e:
                log.error(f"Error scraping extended data for {doc}: {e}")

    @classmethod
    def scrape_all_extended_data(cls, max_dt):
        t_start = time.time()
        for doc_batch in cls.gen_doc_batch_list():
            cls.process_doc_batch(doc_batch)
            dt = time.time() - t_start
            if dt > max_dt:
                log.info(f"🛑 Stopping. {dt:,.1f}s > {max_dt:,}s")
                return
        log.info("🛑 All extended data scraped.")

    def scrape_extended_data_for_doc(self):
        if not os.path.exists(self.text_path):
            self.extract_text()
