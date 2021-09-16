#!/bin/bash
ps -ef | grep celery | awk '{print $2}' | xargs kill -9
nohup celery -A spug beat -l INFO &
nohup celery -A spug worker -l INFO &

