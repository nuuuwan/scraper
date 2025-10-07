FROM python:3.12-slim-bookworm
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
  chromium chromium-driver \
  curl ca-certificates \
  ghostscript git perl \
  libgl1 libglib2.0-0 \
  poppler-utils poppler-data \
  tesseract-ocr tesseract-ocr-eng \
  latexmk \
  texlive-base \
  texlive-latex-base \
  texlive-latex-recommended \
  texlive-latex-extra \
  texlive-fonts-recommended \
  texlive-fonts-extra \
  lmodern \
  texlive-bibtex-extra \
  texlive-publishers \
  && rm -rf /var/lib/apt/lists/*

RUN latexmk -v && kpsewhich lmodern.sty && kpsewhich acl.sty

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app