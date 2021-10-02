#!/bin/bash
ps -ef | grep celery | awk '{print $2}' | xargs kill -9
##ansible null, must export PYTHONOPTIMIZE=1
export PYTHONOPTIMIZE=1
nohup celery -A spug beat -l INFO &
nohup celery -A spug worker -l INFO &

