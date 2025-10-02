# HACK! Delete this once scraper is in pypi

git add . 
git commit -m "various before push_to_clients"
git pull origin main --rebase
git push origin main

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
    "lk_pmd"
    "lk_news"
    "lk_tourism"
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
        git commit -m "[push_to_clients] Deleted scraper"

        rm -rf src/utils_future
        git commit -m "[push_to_clients] Deleted utils_future"

        scraper-nuuuwan >> requiremets.txt
        cat requirements.txt | sort | uniq > requirements.txt.temp
        mv requirements.txt.temp requirements.txt
        
        git add requiremets.txt
        git commit -m "[push_to_clients] Updated requiremets.txt with scraper-nuuuwan"

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