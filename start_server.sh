#!/bin/bash

python manage.py crontab add
sleep 1
python manage.py crontab add
#python manage.py crontab show
#python manage.py crontab remove

python manage.py runserver

