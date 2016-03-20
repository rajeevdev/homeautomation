import web
import json
import threading
import logger
import config

class API():
    def GET(self, id=None):
        if (len(id) == 0):
            return web.notfound()
        elif (id == 'config'):
            web.header('Content-Type', 'application/json')
            web.header('Access-Control-Allow-Origin', '*')
            return json.dumps(config.getJSON())
        elif (id == 'module'):
            web.header('Content-Type', 'application/json')
            web.header('Access-Control-Allow-Origin', '*')
            inputs = web.input(module_id='', action='read')
            if (not inputs.module_id):
                return json.dumps({"error":"module_id missing"})
            return json.dumps(config.getModuleById(inputs.module_id))
        elif (id == 'switch'):
            web.header('Content-Type', 'application/json')
            web.header('Access-Control-Allow-Origin', '*')
            inputs = web.input(module_id='', switch_id='', action='read')
            if (not inputs.module_id):
                return json.dumps({"error":"module_id missing"})
            if (not inputs.switch_id):
                return json.dumps({"error":"switch_id missing"})     
            return json.dumps(config.getSwitchById(inputs.module_id, inputs.switch_id))
        return web.notfound()

    def POST(self, id=None):
        if (id == 'switch'):
            web.header('Content-Type', 'application/json')
            web.header('Access-Control-Allow-Origin', '*')
            inputs = web.input(module_id='', switch_id='', status='', action='read')
            if (not inputs.module_id):
                return json.dumps({"error":"module_id missing"})
            if (not inputs.switch_id):
                return json.dumps({"error":"switch_id missing"})     
            if (not inputs.status):
                return json.dumps({"error":"status missing"})

            APIServer.instance.setSwitchState(inputs.module_id, inputs.switch_id, inputs.status)
            return json.dumps({"error":"success"})

        return web.notfound()

    def DELETE(self, id):
        return web.notfound()

    def PUT(self, id):
        return web.notfound()

class WebApplication(web.application): 
    def run(self, port=8080, *middleware): 
        func = self.wsgifunc(*middleware) 
        return web.httpserver.runsimple(func, ('0.0.0.0', port)) 
              
class APIServer(threading.Thread):
    instance = None
    def __init__(self, server, port):
        logger.info("API Server object created")
        threading.Thread.__init__(self)
        self.port = port
        APIServer.instance = server

    def run(self):    
        logger.info("Starting API server on port: " + str(self.port))
        urls = ('/(.*)', 'API')
        app = WebApplication(urls, globals())
        app.run(port=self.port);
        
        #for t in threads:
        #    t.join()
    
