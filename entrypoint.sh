#!/bin/sh

#entrypoint
python manage.py makemigrations
python manage.py migrate
# python manage.py runserver 0.0.0.0:8000
python Pre_work/pre_run.py
python manage.py runserver 0.0.0.0:8000