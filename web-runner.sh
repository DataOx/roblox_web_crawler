#!/bin/bash
echo 'Start make migrations...'
python -m dao
echo 'Over make migrations...'
uvicorn main:app --host 0.0.0.0 --port 8000
