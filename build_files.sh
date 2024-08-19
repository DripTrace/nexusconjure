#!/usr/bin/env bash

# pip3 install -r requirements.txt
# python3.12 src/manage.py makemigrations --noinput
# python3.12 src/manage.py migrate --noinput
# python3.12 src/manage.py collectstatic --noinput --clear

echo "Installing the latest version of pip..."
python3.12 -m pip install --upgrade pip

# Build the project
echo "Building the project..."
# python3.12 -m pip3 install -r requirements.txt
pip3 install -r requirements.txt

python3.12 src/manage.py makemigrations --noinput
python3.12 src/manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python3.12 src/manage.py collectstatic --noinput --clear