FROM python:3.5

WORKDIR /app

ADD . /app

RUN pip install -r requirements/base.txt

RUN apt-get update && apt-get install -y \
    vim \
    gcc \
    ruby \
    gettext \
    postgresql-client libpq-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENTRYPOINT ["/app/passwd/config/entrypoint.sh"]
