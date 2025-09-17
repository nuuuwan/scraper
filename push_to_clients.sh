# HACK! Delete this once pdf_scraper is in pypi

CLIENT_REPOS=(
    "lk_hansard"
    "lk_appeal_court_judgements"
    "lk_supreme_court_judgements"
)

for CLIENT_REPO in "${CLIENT_REPOS[@]}"; do
    echo "------------------------------------------------------"
    echo "Pushing to $CLIENT_REPO..."
    echo "------------------------------------------------------"

    DIR_CLIENT_REPO="../$CLIENT_REPO"

    [[ -d "$DIR_CLIENT_REPO" ]] || { echo "❌ Missing source dir: $DIR_CLIENT_REPO"; exit 1; }
    
    cd $DIR_CLIENT_REPO;

    git reset --hard HEAD;
    git clean -fd;

    git pull origin main --rebase;

    rm -rf src/pdf_scraper
    cp -r ../pdf_scraper/src/pdf_scraper src/
    git add src/pdf_scraper
    git commit -m "[push_to_clients] Updated pdf_scraper"

    rm -rf src/utils_future
    cp -r ../pdf_scraper/src/utils_future src/
    git add src/utils_future
    git commit -m "[push_to_clients] Updated utils_future"

    git push origin main
    open https://github.com/nuuuwan/$CLIENT_REPO
    echo "✅ Push to $CLIENT_REPO complete."
done


