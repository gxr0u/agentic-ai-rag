#!/bin/bash
echo "Starting deployment startup script"

pip install --upgrade pip
pip install -r /home/site/wwwroot/requirements.txt

exec gunicorn app.main:app \
  --workers 1 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 600
