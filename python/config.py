#<Config>
#   <SystemId>1234567890</SystemId>
#   <Modules>
#      <Module>
#         <ModuleId>11-22-33-44-55-66</ModuleId>
#         <Switch>
#            <SwitchId>gpio0</SwitchId>
#            <Status>0</Status>
#         </Switch>
#         <Switch>
#            <SwitchId>gpio2</SwitchId>
#            <Status>0</Status>
#         </Switch>
#      </Module>
#      <Module>
#         <ModuleId>11-22-33-44-55-77</ModuleId>
#         <Switch>
#            <SwitchId>gpio0</SwitchId>
#            <Status>0</Status>
#         </Switch>
#         <Switch>
#            <SwitchId>gpio2</SwitchId>
#            <Status>0</Status>
#         </Switch>
#      </Module>
#   </Modules>
#</Config>

#{
#    "Config": {
#        "SystemId": "1234567890",
#        "Modules": {
#            "Module": [
#                {
#                    "ModuleId": "11-22-33-44-55-66",
#                    "Status": "1",
#                    "Switch": [
#                        {
#                            "SwitchId": "gpio0",
#                            "Status": "0"
#                        },
#                        {
#                            "SwitchId": "gpio2",
#                            "Status": "0"
#                        }
#                    ]
#                },
#                {
#                    "ModuleId": "11-22-33-44-55-77",
#                    "Status": "1",
#                    "Switch": [
#                        {
#                            "SwitchId": "gpio0",
#                            "Status": "0"
#                        },
#                        {
#                            "SwitchId": "gpio2",
#                            "Status": "0"
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

class Config(object):
    instance = None
    def __init__(self):
        systemId = ""
        try:
            print "Reading configuration"
            fd = os.open( "system.conf", os.O_RDONLY)
            jsonString = ""
            while True:
                data = os.read(fd, 2048)
                if (not data):
                    break
                jsonString += data

            self.json = json.loads(jsonString)
            
            # Reset status to "0" for all module
            for module in self.json['Config']['Modules']['Module']:
                module['Status'] = "0"

        except:
            systemId = str(uuid.uuid1())
            self.json = {}
            self.json['Config'] = {}
            self.json['Config']['SystemId'] = systemId
            self.json['Config']['Modules'] = {}
            self.json['Config']['Modules']['Module'] = []

            fd = os.open( "system.conf", os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
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
    js = getInstance().json
    getInstance().lock.release()
    return json.dumps(js, indent=1, sort_keys=True)
    
def updateModule(moduleId, status):
    getInstance().lock.acquire()
    try:
        # Check if module with moduleId exists
        for module in getInstance().json['Config']['Modules']['Module']:
            if module['ModuleId'] == moduleId:
                module['Status'] = status
                break
    except:
        print("Error in updating config")

    fd = os.open( "system.json", os.O_WRONLY | os.O_TRUNC)
    os.write(fd, json.dumps(getInstance().json, indent=1, sort_keys=True))
    os.close(fd)
    #updateStatus();
    getInstance().lock.release()
    
def updateSwitch(moduleId, switchId, status):
    getInstance().lock.acquire()
    try:
        # Check if module with moduleId exists
        moduleFound = False
        for module in getInstance().json['Config']['Modules']['Module']:
            module['Status'] = "1"
            if module['ModuleId'] == moduleId:
                switchFound = False
                # Check if switch with switchId exists
                for switch in module['Switch']:
                    if switch['SwitchId'] == switchId:
                        switch['Status'] = status
                        switchFound = True

                if (not switchFound):
                    module['Switch'].append({'SwitchId': switchId, 'Status': status})

                moduleFound = True
                break

        # if not then create it
        if (not moduleFound):
            getInstance().json['Config']['Modules']['Module'].append({'ModuleId': moduleId, "Status": "1", 'Switch': []})
            getInstance().json['Config']['Modules']['Module'][-1]['Switch'].append({'SwitchId': switchId, 'Status': status})            
    except:
        print("Error in updating config")

    fd = os.open( "system.json", os.O_WRONLY | os.O_TRUNC)
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
    