#!/bin/sh
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 #runworker -v 2 #runserver_plus 0.0.0.0:8000
