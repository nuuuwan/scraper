# HACK! Delete this once pdf_scraper is in pypi

CLIENT_REPOS=(
    "lk_hansard"
    "lk_judiciary_appeals_court"
    "lk_supreme_court_judgements"
)

for CLIENT_REPO in "${CLIENT_REPOS[@]}"; do
    echo "------------------------------------------------------"
    echo "Pushing to $CLIENT_REPO"
    echo "------------------------------------------------------"

    DIR_CLIENT_REPO="../$CLIENT_REPO"
    
    cd $DIR_CLIENT_REPO;

    git reset --hard HEAD;
    git clean -fd;

    cp ../pdf_scraper/copy_from_pdf_scraper.sh .
    git add copy_from_pdf_scraper.sh
    git commit -m "[push_to_clients] Updated copy_from_pdf_scraper.sh"

    rm -rf src/pdf_scraper
    cp -r ../pdf_scraper/src/pdf_scraper src/
    git add src/pdf_scraper
    git commit -m "[push_to_clients] Updated pdf_scraper"

    rm -rf src/utils_future
    cp -r ../pdf_scraper/src/utils_future src/
    git add src/utils_future
    git commit -m "[push_to_clients] Updated utils_future"
done


