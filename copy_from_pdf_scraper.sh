# HACK! Delete this once pdf_scrape is in pypi
rm -rf src/pdf_scraper
cp -r ../pdf_scraper/src/pdf_scraper src/
git add src/pdf_scraper
git commit -m "[copy_from_pdf_scraper] Updated pdf_scraper"

rm -rf src/utils_future
cp -r ../pdf_scraper/src/utils_future src/
git add src/utils_future
git commit -m "[copy_from_pdf_scraper] Updated utils_future"


