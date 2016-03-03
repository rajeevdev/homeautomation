from flask import Flask, jsonify, request
import config

app = Flask(__name__)

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify(config.getJson())

@app.route('/module', methods=['GET'])
def process_module():
    module_id = request.args.get('module_id', '')
    if (not module_id):
        return jsonify({"error", "module_id missing"})
    return jsonify(config.getModuleById(module_id))
    
@app.route('/switch', methods=['GET', 'POST'])
def process_switch():
    module_id = request.args.get('module_id', '')
    switch_id = request.args.get('switch_id', '')
    
    if (not module_id or not switch_id):
        return jsonify({"error", "module_id or switch_id missing"})
    
    if request.method == 'POST':
        jsonData = request.get_json()
        status = jsonData['status']
        if (not status):
            return jsonify({"error", "status missing"})
        config.updateSwitch(module_id, switch_id, status)
        
    return jsonify(config.getSwitchById(module_id, switch_id))

def start():    
    app.run(host="0.0.0.0", port=int("8080"))
