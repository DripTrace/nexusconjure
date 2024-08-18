#!/usr/bin/env bash

pip3 install -r requirements.txt
python3.12 src/manage.py makemigrations --noinput
python3.12 src/manage.py migrate --noinput
python3.12 src/manage.py collectstatic --noinput