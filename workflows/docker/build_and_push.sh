#!/usr/bin/env bash
set -euo pipefail

echo '--------------------------------------'

docker --version

docker system df
docker system prune -f
docker system prune -a --volumes -f
docker builder prune -a -f 

echo '--------------------------------------'

URL=ghcr.io/$GITHUB_USERNAME/pdf-scraper-image:latest
echo "URL=$URL"

docker buildx inspect multiarch-builder >/dev/null 2>&1 || \
  docker buildx create --name multiarch-builder --use

docker buildx use multiarch-builder

docker buildx build \
  -f workflows/docker/Dockerfile \
  --platform linux/amd64,linux/arm64 \
  -t "$URL" \
  --push \
  .

echo '--------------------------------------'

echo 'Validating Python Version...'
if ! docker run --rm "$URL" python --version; then
  echo "❌ ERROR: Python version check failed for image: $URL" >&2
  exit 1
fi
echo '✅ Python version check passed.'

echo '--------------------------------------'

docker system df
# docker system prune -f
# docker system prune -a --volumes -f
# docker builder prune -a -f 
# docker system df

echo '--------------------------------------'

say "docker build and push complete!"
open "https://github.com/users/$GITHUB_USERNAME/packages/container/pdf-scraper-image/versions"

echo '--------------------------------------'
