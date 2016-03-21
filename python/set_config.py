import threading
import time
import requests
import json
import logger
import config
import sys

class SetStatus(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        logger.info("Waiting for 10 seconds before starting SET CONFIG loop...")
        system_id = config.getSystemId()
        #print system_id
        time.sleep(10)
        
        while True:
            try:
                logger.info("Updating status...")
                jsonConfig = config.getJSON()
                url = 'http://homemonitor.esy.es/php/api.php?request=set_config&system_id=' + system_id
                resp = requests.post(url, json=jsonConfig)
                if resp.status_code == 200:
                    logger.info("Config Successfully updated")
                else:
                    print resp.json();

            except requests.exceptions.RequestException as e:
                print e;
            except:
                print "Unexpected error: ", sys.exc_info()[0]

            time.sleep(15)