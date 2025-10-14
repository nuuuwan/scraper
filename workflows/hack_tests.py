from scraper import AbstractExcelSpreadsheet

if __name__ == "__main__":
    doc = AbstractExcelSpreadsheet(
        num="1234567890",
        date_str="2023-10-01",
        description="Test Document",
        url_metadata="http://mock.com/doc.html",
        lang="en",
        url_excel="https://raw.githubusercontent.com/nuuuwan"
        + "/scraper/refs/heads/main"
        + "/tests/input/test.xlsx",
    )
    doc.scrape_extended_data_for_doc()
