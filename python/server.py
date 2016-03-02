#!/usr/bin/env python

# COMMANDS:
# ---------
# [GET /moduleId]
# [/moduleId/48-2C-6A-1E-59-3D]
#
# [GET /gpio0]
# [/gpio0/0]
#
# [GET /gpio2]
# [/gpio2/0]
#
# [SET /gpio0/1]
# [OK]
#
# [SET /gpio0/0]
# [OK]
#
# [SET /gpio2/1]
# [OK]
#
# [SET /gpio2/0]
# [OK]

#import requests
#import json
#import argparse
#import time  # this is only being used as part of the example
#import logger
import logger
import config
import server_socket
import get_command
import json;

#import set_status
#import requests
#data = "[/gpio0/0][/gpio0/1]["
#startIndex = data.find("[");
#endIndex = data.find("]");
#packet = data[startIndex:endIndex+1];
#data = data[endIndex+1:]
#print data

#resp = requests.get('http://homemonitor.esy.es/api.php?request=get_status&system_id=1234567890')
#print resp
#exit();

#j = {}
#j['Config'] = {}
#j['Config']['SystemId'] = '1234567890'
#j['Config']['Modules'] = {}
#j['Config']['Modules']['Module'] = []
#print json.dumps(j, indent=4, sort_keys=True)

#for t in j['Config']['Modules']['Module']:
#   if t['NodeId'] == nodeId:
#      t['State'] = '1'
      
#if m in j['Config']['Modules']
#    print m
#exit();

logger.setupLogger();
logger.info("========== DEVICE SERVER STARTED ==========")

# Dummy call to initialize the config object
logger.info("Starting server with configuration:\n" + config.getString())

#print config.getString()
#config.updateModule("11-11-11-11-11-11", "relay1", "1")
#print config.getString()
#config.updateModule("11-11-11-11-11-11", "relay1", "0")
#print config.getString()
#config.updateModule("11-11-11-11-11-11", "relay2", "0")
#config.updateModule("11-11-11-11-11-11", "relay2", "1")
#print config.getString()
#config.updateModule("22-11-11-11-11-11", "relay2", "1")
#config.updateModule("22-11-11-11-11-11", "relay1", "1")
#config.updateModule("11-11-11-11-11-11", "relay1", "2")
#print config.getString()
#exit();


print "Staring server thread\n"
server = server_socket.Server("0.0.0.0", 9000)
server.start();
print "Server thread started\n"

print "Staring command handler thread\n"
commandHandler = get_command.GetCommand(server)
#commandHandler.start();
print "Command handler thread started\n"

# switch_states = [
                    # {"switch_id":"0","status":"1"},
                    # {"switch_id":"1","status":"1"}
                # ]

# while True:
    # try:
        # print "Sending:" + json.dumps(switch_states)
        # resp = requests.post('http://homemonitor.esy.es/api.php?request=set_status&system_id=1234567890',json=switch_states)

        # if resp.status_code == 200:
            # logger.info("Success")
        # else:
            # logger.error("Could not set status")

    # except requests.exceptions.RequestException as e:
        # print e;
    # except:
        # print "Unexpected error: ", sys.exc_info()[0]
    
    # time.sleep(10)

