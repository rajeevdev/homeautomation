from flask import Flask, jsonify, request
#import web
#import json
import config

app = Flask(__name__)

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify(config.getJson())

@app.route('/module', methods=['GET'])
def process_module():
    module_id = request.args.get('module_id', '')
    return jsonify(config.getModuleById(module_id))
    
@app.route('/switch', methods=['GET', 'POST'])
def process_switch():
    module_id = request.args.get('module_id', '')
    switch_id = request.args.get('switch_id', '')
    if request.method == 'POST':
        status = request.args.get('status', '')
        return jsonify({"updated": "true"})
    return jsonify({"module_id": "11-11-11-11-11-11", "switch_id": "relay1"})

def start():    
    app.run(host="0.0.0.0", port=int("8080"))

#class GetStatus():
#    def GET(self):
#        output = config.getString()
#        web.header('Content-Type', 'application/json')
#        web.header('Access-Control-Allow-Origin', '*')
#        return output

#class GetModuleById():
#    def GET(self, moduleId):
#        output = config.getModuleById(moduleId)
#        web.header('Content-Type', 'application/json')
#        web.header('Access-Control-Allow-Origin', '*')          
#        return output;

#class SwitchHandler():
#    def POST(self):
#        print "POST"
#        #print web.data()
#        return "{}"
          #output = config.getModuleById(moduleId)
          #web.header('Content-Type', 'application/json')
          #web.header('Access-Control-Allow-Origin', '*')          
          #return output;
    #def GET(self):
    #    print "GET"
    #    return "{}"
#class get_user:
#     def GET(self, user):
#          for child in root:
#               if child.attrib['id'] == user:
#                    return str(child.attrib)


#class APIServer(web.application):
#    def __init__(self):
#        app = Flask(__name__)
        #self.app = web.application(urls, globals())
 
    #def start(self):
     #   app.run(debug=True)