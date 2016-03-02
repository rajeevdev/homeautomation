import threading
import time
import requests
import json
import logging
import logging.handlers
import sys
import server_socket

class SetStatus(threading.Thread):
    def __init__(self, server = server_socket.Server):
        threading.Thread.__init__(self)
        self.server = server

    def run(self):
        print "Starting Status loop ..."
            try:
                print "Geting command state"
                resp = requests.get('http://homemonitor.esy.es/api.php?request=get_status&system_id=1234567890')
                if resp.status_code == 200:
                    print "Success"
                   
                    switch_states = resp.json()
                    for item in switch_states:
                        print item['switch_id']
                        print item['status']
                        print item['current_cmd']

                       ###############
                       # Execute command

                       #item['current_cmd'] = 0 #Reset current_cmd to 0

                   #print "Sending:" + json.dumps(switch_states)
                   #resp = requests.post('http://homemonitor.esy.es/api.php?request=set_command&system_id=1234567890',json=switch_states)
                   #if resp.status_code == 200:
                   #    logger.info("Command state updated")
                   #else:
                   #    logger.error("Error updating command state")
                else:
                    logger.error("Error getting command status")
            except requests.exceptions.RequestException as e:
                print e;
            except:
                print "Unexpected error: ", sys.exc_info()[0]
        

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

