# HACK! Delete this once scraper is in pypi

CLIENT_REPOS=(
    "lk_cabinet_decisions"
    "lk_datasets"
    "lk_hansard"
    "lk_appeal_court_judgements"
    "lk_supreme_court_judgements"
    "lk_police_press_releases"
    "lk_legal_docs"    
    # "lk_parliament_members"
    "lk_treasury"
)

function push_to_client_repo() {
    local CLIENT_REPO="$1"
    
    function inner() {
        DIR_CLIENT_REPO="../$CLIENT_REPO"

        [[ -d "$DIR_CLIENT_REPO" ]] || { echo "❌ Missing source dir: $DIR_CLIENT_REPO"; exit 1; }
        
        cd "$DIR_CLIENT_REPO" || exit 1

        git reset --hard HEAD
        git clean -fd

        mkdir -p src

        git pull origin main --rebase

        rm -rf src/scraper
        cp -r ../scraper/src/scraper src/
        git add src/scraper
        git commit -m "[push_to_clients] Updated scraper"

        rm -rf src/utils_future
        cp -r ../scraper/src/utils_future src/
        git add src/utils_future
        git commit -m "[push_to_clients] Updated utils_future"

        git push origin main

        # open https://github.com/nuuuwan/$CLIENT_REPO/actions/workflows/pipeline.yml
        # code $DIR_CLIENT_REPO
    }
    inner > /dev/null 2>&1 

    echo "✅ Push to $CLIENT_REPO complete."
}

for CLIENT_REPO in "${CLIENT_REPOS[@]}"; do
    push_to_client_repo "$CLIENT_REPO" &
done


wait
echo "✅✅ ALL pushes complete."