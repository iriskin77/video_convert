#!/bin/sh

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 10
done
python manage.py runserver 0.0.0.0:8044
