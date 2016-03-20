#!/usr/bin/env python

import requests
import json
import pprint
import sys
import time  # this is only being used as part of the example

while True:
    print "Geting command"
    resp = requests.get('http://homemonitor.esy.es/api.php?request=get_status&system_id=1234567890')

    for item in resp.json():
        print item['switch_id']
        print item['status']

    # Execute command

    time.sleep(10)


#resp = requests.get('http://homemonitor.esy.es/api.php?request=get_status&system_id=1234567890')
#print resp
#if resp.status_code != 200:
#    # This means something went wrong.
#    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
#for item in resp.json():
#    print item['system_id']
#    print item['switch_id']
#    print item['status']

