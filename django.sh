#!/bin/bash

python3 manage.py makemigrations merge --noinput

python3 manage.py makemigrations --noinput

python3 manage.py migrate

python3 manage.py runserver