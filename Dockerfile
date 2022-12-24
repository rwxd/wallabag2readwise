FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

RUN : \
    pip --no-cache-dir install -r requirements.txt

COPY . .

RUN pip install .

ENTRYPOINT ["wallabag2readwise", "daemon"]
