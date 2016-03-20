import threading
import time
import requests
import json
import logger
import sys
import server_socket

class GetCommand(threading.Thread):
    def __init__(self, server = server_socket.Server):
        threading.Thread.__init__(self)
        self.server = server

    def run(self):
        logger.info("Starting Command loop ...")
        while True:
            try:
                logger.info("Geting command state")
                resp = requests.get('http://homemonitor.esy.es/api.php?request=get_status&system_id=1234567890')
                if resp.status_code == 200:
                    logger.info("Success")
                   
                    switch_states = resp.json()
                    for item in switch_states:
                        logger.info(item['switch_id'])
                        logger.info(item['status'])
                        logger.info(item['current_cmd'])

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
                logger.info(e);
            except:
                logger.info("Unexpected error: ", sys.exc_info()[0])

            time.sleep(10)
