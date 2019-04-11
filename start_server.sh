#!/bin/bash

function refresh_crontab() {
	python manage.py crontab add
}

function print_crontab() {
	python manage.py crontab show
}

function cleanup() {
	python manage.py crontab remove
	echo Clean up done
	exit 1
}


# Preparation
trap 'cleanup' SIGINT
refresh_crontab
sleep 1
refresh_crontab
print_crontab

# Running
python manage.py runserver

# Ending cleanup
cleanup

