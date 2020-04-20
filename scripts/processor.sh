#!/bin/sh
set -e
set -x

cd /code
while :
do
  echo "$(date) - starting processing"
  python manage.py process
  echo "$(date) - processing ended"
  sleep 120
done