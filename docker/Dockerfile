FROM python:3.12-slim-bookworm
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
  chromium \
  chromium-driver \
  curl ca-certificates \
  ghostscript git \
  libgl1 libglib2.0-0 \
  poppler-utils poppler-data \
  tesseract-ocr tesseract-ocr-eng \
  && rm -rf /var/lib/apt/lists/*

ENV OMP_THREAD_LIMIT=4
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app