#!/bin/bash
echo 'Start make migrations...'
echo "Waiting for postgres..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_INTERNAL_PORT; do
    sleep 0.1
  done
echo "Postgres started"

python -m dao

echo 'Successfully migrations'
uvicorn main:app --host 0.0.0.0 --port 8000
