#!/bin/bash

set -xe

# check if we already have the celeryd service
supervisorctl -c /opt/python/etc/supervisord.conf status | grep celeryd
if [[ $? ]]; then
  supervisorctl -c /opt/python/etc/supervisord.conf restart celeryd
fi

eventHelper.py --msg "Application server successfully restarted." --severity INFO