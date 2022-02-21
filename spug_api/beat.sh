#!/bin/bash
#ps -ef | grep beat | awk '{print $2}' | xargs kill -9
##ansible null, must export PYTHONOPTIMIZE=1
export PYTHONOPTIMIZE=1
cd /data/spug/spug_api && celery -A spug beat -l INFO  --scheduler django_celery_beat.schedulers:DatabaseScheduler
