FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE treasure_hunting.settings.production
ENV SECRET_KEY _
ENV ALLOWED_HOSTS localhost

ENV HTTP_HOST 0.0.0.0
ENV HTTP_PORT 80

ENV DATABASE_ENGINE django.db.backends.postgresql
ENV DATABASE_NAME postgres
ENV DATABASE_HOST postgres
ENV DATABASE_PORT 5432

RUN apk add libc-dev gcc postgresql-dev postgresql-client

RUN mkdir /app
WORKDIR /app

COPY . /app/
RUN pip install -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 80
