#!/usr/bin/env bash
set -euo pipefail

docker --version

docker system df
docker system prune -f
docker system prune -a --volumes -f
docker builder prune -a -f 

URL=ghcr.io/$GITHUB_USERNAME/pdf-scraper-image:latest
echo "URL=$URL"

docker buildx inspect multiarch-builder >/dev/null 2>&1 || \
  docker buildx create --name multiarch-builder --use

docker buildx use multiarch-builder

docker buildx build \
  -f docker/Dockerfile \
  --platform linux/amd64,linux/arm64 \
  -t "$URL" \
  --push \
  .

echo 'Validating Python Version...'
docker run --rm "$URL" python --version

say "docker build and push complete!"
open https://github.com/$GITHUB_USERNAME?tab=packages