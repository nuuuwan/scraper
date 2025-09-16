import time

from utils import Log

log = Log("PipelineExtendedDataMixin")


class PipelineExtendedDataMixin:
    def scrape_extended_data(self, max_dt):
        t_start = time.time()
        doc_list = self.doc_class.list_all()
        for doc in doc_list:
            try:
                doc.scrape_extended_data()
            except Exception as e:
                log.error(f"Error scraping extended data for {doc}: {e}")

            dt = time.time() - t_start
            if dt > max_dt:
                log.info(f"🛑 Stopping. {dt:,.1f}s > {max_dt:,}s")
                return
        log.info("🛑 All extended data scraped.")
