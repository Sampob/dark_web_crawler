#!/bin/bash
service tor start
service privoxy start

sleep 1

exec su -c "celery -A app.celery_config worker --max-tasks-per-child=1" celeryworker