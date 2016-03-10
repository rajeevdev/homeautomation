from flask import Flask, jsonify, request, make_response, current_app
from functools import update_wrapper
from datetime import timedelta
import config

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__)
server = None

@app.route('/config', methods=['GET'])
@crossdomain(origin='*')
def get_config():
    return jsonify(config.getJson())

@app.route('/module', methods=['GET'])
@crossdomain(origin='*')
def process_module():
    module_id = request.args.get('module_id', '')
    if (not module_id):
        return jsonify({"error":"module_id missing"})
    return jsonify(config.getModuleById(module_id))
    
@app.route('/switch', methods=['GET', 'POST'])
@crossdomain(origin='*')
def process_switch():

    module_id = request.args.get('module_id', '')
    switch_id = request.args.get('switch_id', '')
    
    if (not module_id):
        return jsonify({"error":"module_id missing"})
    if (not switch_id):
        return jsonify({"error":"switch_id missing"})
     
    if request.method == 'GET':
        return jsonify(config.getSwitchById(module_id, switch_id))

    if request.method == 'POST':
        status = request.args.get('status', '')
        if (not status):
            return jsonify({"error":"status missing"})

        server.setSwitchState(module_id, switch_id, status)
        return jsonify({"error":"success"})
        
    return jsonify({"error":"unknown request"})
    
def start():
    app.run(host="0.0.0.0", port=int("9999"),use_reloader=False)
