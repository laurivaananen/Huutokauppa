#!/bin/bash

source /opt/python/current/env
source /opt/python/run/venv/bin/activate
cd /opt/python/current/app
# Note: exec is important here - this way supervisord will control
# the python script and not the bash script
#
exec /opt/python/run/venv/bin/celery worker -A /opt/python/current/app/application -l info --config=/opt/python/current/app/celery_config