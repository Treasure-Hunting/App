#!/bin/sh

echo "Waiting for PostgreSQL"
while ! pg_isready -h $DATABASE_HOST -p $DATABASE_PORT -U $DATABASE_USER -d $DATABASE_NAME
do
  sleep 1
done

python manage.py migrate
python manage.py loaddata initial_data
python manage.py runserver $HOST:$PORT
