#<config>
#   <system_id>1234567890</system_id>
#   <modules>
#      <module>
#         <module_id>11-22-33-44-55-66</module_id>
#         <switch>
#            <switch_id>gpio0</switch_id>
#            <status>0</status>
#         </switch>
#         <switch>
#            <switch_id>gpio2</switch_id>
#            <status>0</status>
#         </switch>
#      </module>
#      <module>
#         <module_id>11-22-33-44-55-77</module_id>
#         <switch>
#            <switch_id>gpio0</switch_id>
#            <status>0</status>
#         </switch>
#         <switch>
#            <switch_id>gpio2</switch_id>
#            <status>0</status>
#         </switch>
#      </module>
#   </modules>
#</config>

#{
#    "config": {
#        "system_id": "1234567890",
#        "modules": {
#            "module": [
#                {
#                    "module_id": "11-22-33-44-55-66",
#                    "status": "1",
#                    "switch": [
#                        {
#                            "switch_id": "gpio0",
#                            "status": "0"
#                        },
#                        {
#                            "switch_id": "gpio2",
#                            "status": "0"
#                        }
#                    ]
#                },
#                {
#                    "module_id": "11-22-33-44-55-77",
#                    "status": "1",
#                    "switch": [
#                        {
#                            "switch_id": "gpio0",
#                            "status": "0"
#                        },
#                        {
#                            "switch_id": "gpio2",
#                            "status": "0"
#                        }
#                    ]
#                }
#            ]
#        }
#    }
#}

import uuid
import threading;
import json
import logger
import os
import sys
import requests

CONFIG_FILE = "../config/system.json"
class Config(object):
    instance = None
    def __init__(self):
    
        if not os.path.exists(os.path.dirname(CONFIG_FILE)):
            try:
                os.makedirs(os.path.dirname(CONFIG_FILE))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
    
        systemId = ""
        try:
            print "Reading configuration"
            fd = os.open( CONFIG_FILE, os.O_RDONLY)
            jsonString = ""
            while True:
                data = os.read(fd, 2048)
                if (not data):
                    break
                jsonString += data

            self.json = json.loads(jsonString)
            
            # Reset status to "0" for all module
            for module in self.json['config']['modules']['module']:
                module['status'] = "0"

        except:
            systemId = str(uuid.uuid1())
            self.json = {}
            self.json['config'] = {}
            self.json['config']['system_id'] = systemId
            self.json['config']['modules'] = {}
            self.json['config']['modules']['module'] = []

            fd = os.open( CONFIG_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
            os.write(fd, json.dumps(self.json, indent=1, sort_keys=True))
            os.close(fd)

        self.lock = threading.Lock()

def getInstance():
    if Config.instance == None:
        Config.instance = Config()
    return Config.instance

def getJson():
    getInstance().lock.acquire()
    js = Config.instance.json
    Config.instance.lock.release()
    return js

def getString():
    getInstance().lock.acquire()
    jsonObject = getInstance().json
    getInstance().lock.release()
    return json.dumps(jsonObject)
    
def getFormattedString():
    getInstance().lock.acquire()
    jsonObject = getInstance().json
    getInstance().lock.release()
    return json.dumps(jsonObject, indent=1, sort_keys=True)
    
def updateModule(moduleId, status):
    getInstance().lock.acquire()
    try:
        # Check if module with moduleId exists
        for module in getInstance().json['config']['modules']['module']:
            if module['module_id'] == moduleId:
                print "update for " + moduleId
                module['status'] = status
                break
    except:
        print("Error in updating config")

    fd = os.open( CONFIG_FILE, os.O_WRONLY | os.O_TRUNC)
    os.write(fd, json.dumps(getInstance().json, indent=1, sort_keys=True))
    os.close(fd)
    #updateStatus();
    getInstance().lock.release()

def getModuleById(moduleId):
    getInstance().lock.acquire()
    reply = {}
    try:
        # Check if module with moduleId exists
        for module in getInstance().json['config']['modules']['module']:
            if module['module_id'] == moduleId:
                reply = module
                break
    except:
        print("Error in getting module")
    getInstance().lock.release()
    return reply

def getSwitchById(moduleId, switchId):
    getInstance().lock.acquire()
    reply = {}
    try:
        # Check if module with moduleId exists
        for module in getInstance().json['config']['modules']['module']:
            if module['module_id'] == moduleId:
                for switch in module['switch']:
                    if switch['switch_id'] == switchId:
                        reply = switch
                        break
                break
    except:
        print("Error in getting switch")
    getInstance().lock.release()
    return reply
    
def updateSwitch(moduleId, switchId, status):
    getInstance().lock.acquire()
    try:
        # Check if module with moduleId exists
        moduleFound = False
        for module in getInstance().json['config']['modules']['module']:
            if module['module_id'] == moduleId:
                moduleFound = True
                module['status'] = "1"
                
                switchFound = False
                # Check if switch with switchId exists
                for switch in module['switch']:
                    if switch['switch_id'] == switchId:
                        switch['status'] = status
                        switchFound = True

                if (not switchFound):
                    module['switch'].append({'switch_id': switchId, 'status': status})

                break

        # if not then create it
        if (not moduleFound):
            getInstance().json['config']['modules']['module'].append({'module_id': moduleId, "status": "1", 'switch': []})
            getInstance().json['config']['modules']['module'][-1]['switch'].append({'switch_id': switchId, 'status': status})            
    except:
        print("Error in updating config")

    fd = os.open( CONFIG_FILE, os.O_WRONLY | os.O_TRUNC)
    os.write(fd, json.dumps(getInstance().json, indent=1, sort_keys=True))
    os.close(fd)
    #updateStatus();
    getInstance().lock.release()
    
def updateStatus():
        switch_states = [
                            {"switch_id":"gpio0","status":str(gpio0)},
                            {"switch_id":"gpio2","status":str(gpio2)}
                        ]
        try:
            logger.info("Sending:" + json.dumps(switch_states))
            resp = requests.post('http://homemonitor.esy.es/api.php?request=set_status&system_id=1234567890',json=switch_states)

            if resp.status_code == 200:
                logger.info("Status updated successfully")
            else:
                logger.error("Failed to update status")

        except requests.exceptions.RequestException as e:
            logger.info(e);
        #except:
        #    print "Unexpected error: ", sys.exc_info()[0]
    