import web
import json
import config

urls = (
     #'/getStatus', 'GetStatus',
     #'/getStatus/SystemId', 'GetSystemId',
     #'/getModule/(.*)', 'GetModuleById',
     'setSwitchState', 'SetSwitchState'
     #'/users/(.*)', 'get_user'
)

class GetStatus():
    def GET(self):
        output = config.getString()
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        return output

class GetModuleById():
    def GET(self, moduleId):
        output = config.getModuleById(moduleId)
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')          
        return output;

class SetSwitchState():
    def POST(self):
        print "Here"
        #print web.data()
        return "{}"
          #output = config.getModuleById(moduleId)
          #web.header('Content-Type', 'application/json')
          #web.header('Access-Control-Allow-Origin', '*')          
          #return output;
    def GET(self):
        print "Here 2"
        return "{}"
#class get_user:
#     def GET(self, user):
#          for child in root:
#               if child.attrib['id'] == user:
#                    return str(child.attrib)


class APIServer(web.application):
    def __init__(self):
        self.app = web.application(urls, globals())
 
    def start(self):
        self.app.run()