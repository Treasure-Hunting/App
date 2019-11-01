FROM python:3-alpine

ENV PYTHONUNBUFFERED="1" \
    DJANGO_SETTINGS_MODULE="treasure_hunting.settings.production" \
    SECRET_KEY="_" \
    ALLOWED_HOSTS="localhost" \
    HOST="0.0.0.0" \
    PORT="80" \
    DATABASE_ENGINE="django.db.backends.postgresql" \
    DATABASE_NAME="postgres" \ 
    DATABASE_HOST="postgres" \
    DATABASE_PORT="5432" \
    DATABASE_USER="postgres" \
    DATABASE_PASSWORD=""

RUN set -x && \
    apk upgrade --no-cache && \
    apk add --no-cache libc-dev \
                       gcc \
                       postgresql-dev \
                       postgresql-client

ARG project_dir=/app
WORKDIR ${project_dir}
COPY . ${project_dir}

RUN pip install -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 80
