#!/bin/bash
celery -A spug beat -l INFO
celery -A spug worker -l INFO

