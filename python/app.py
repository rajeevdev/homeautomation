#!/usr/bin/env python

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify({"Config", {}})

@app.route('/module', methods=['GET'])
def process_module():
    module_id = request.args.get('module_id', '')
    return jsonify({"module_id": "11-11-11-11-11-11"})
    
@app.route('/switch', methods=['GET', 'POST'])
def process_switch():
    module_id = request.args.get('module_id', '')
    switch_id = request.args.get('switch_id', '')
    if request.method == 'POST':
        status = request.args.get('status', '')
        return jsonify({"updated": "true"})
    return jsonify({"module_id": "11-11-11-11-11-11", "switch_id": "relay1"})

if __name__ == '__main__':
    app.run(debug=True)