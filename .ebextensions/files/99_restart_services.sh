#!/bin/bash

set -xe

# check if we already have the celeryd service
/usr/bin/supervisorctl -c /opt/python/etc/supervisord.conf status | grep celeryd
if [[ $? ]]; then
  /usr/bin/supervisorctl -c /opt/python/etc/supervisord.conf restart celeryd
fi

eventHelper.py --msg "Application server successfully restarted." --severity INFO