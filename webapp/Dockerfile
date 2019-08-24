FROM python:3.6.4
ARG env=prod

WORKDIR /app

ADD . /app

RUN mkdir /env \
    && touch /env/secrets.env

RUN pip install -r requirements/base.txt

RUN if [ "$env" = "dev" ]; then pip install -r requirements/dev.txt; fi

RUN apt-get update && apt-get install -y \
    vim \
    gcc \
    gettext \
    libav-tools \
    postgresql-client libpq-dev \
    --no-install-recommends

RUN pip install awscli

RUN rm -rf /var/lib/apt/lists/*

EXPOSE 8000 5555

ENTRYPOINT ["/app/entrypoint/entrypoint.sh"]
