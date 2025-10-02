#!/usr/bin/env bash

# -e: exit immediately if any command fails
# -u: treat unset variables as an error
# -o pipefail: make pipelines fail if any command fails
set -euo pipefail

# Sanity check Docker
docker --version

URL=ghcr.io/$GITHUB_USERNAME/pdf-scraper-image:latest
echo "URL=$URL"

# Check if a buildx builder called "multiarch-builder" exists
# If not, create it and set it as the default builder
docker buildx inspect multiarch-builder >/dev/null 2>&1 || \
  docker buildx create --name multiarch-builder --use

# Explicitly use the "multiarch-builder"
docker buildx use multiarch-builder

# Build the Docker image using buildx
# -f docker/Dockerfile → specify which Dockerfile to use
# --platform → build for both amd64 and arm64 (multi-architecture)
# -t "$URL" → tag the image with the registry URL
# --push → push the built image directly to the registry
# . → build context is the current directory
docker buildx build \
  -f docker/Dockerfile \
  --platform linux/amd64,linux/arm64 \
  -t "$URL" \
  --push \
  .

# Run the built image, check the Python version inside it
# --rm → remove the container after it finishes
echo 'Validating Python Version...'
docker run --rm "$URL" python --version



# Open the GitHub Packages page in the default browser 
say "docker build and push complete!"
open https://github.com/$GITHUB_USERNAME?tab=packages