#!/usr/bin/env bash
#!/bin/sh
set -e
set -x

cd /code
while :
do
  echo "$(date) - collecting started"
  python manage.py collect
  echo "$(date) - collecting ended"
  sleep 120
done