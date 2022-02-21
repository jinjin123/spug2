#!/bin/bash
ps -ef | grep celery | awk '{print $2}' | xargs kill -9
##ansible null, must export PYTHONOPTIMIZE=1
#cd /data/spug/spug_api/
export PYTHONOPTIMIZE=1
nohup  celery -A spug beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler &
nohup  celery -A spug worker -l INFO  &

