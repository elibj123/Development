import logging

from Python.AltTV.ProcessMonitor import ProcessMonitor
from Python.AltTV.RestUtils import json_obj_response, json_string_response
from Python.AltTV.core.Monitors import Monitors
from flask import Flask, request, send_from_directory
from flask_cors import CORS

import Python.AltTV.server.LoggerFactory

app = Flask('ProcessMonitor')
app.debug = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
monitors = Monitors(persistence_file="files/data/monitors.json")


def start_rest_server():
    for handler in Python.AltTV.server.LoggerFactory.get_logger_handler(['files/logs/rest_server_log.json']):
        app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.run(host='127.0.0.1', port='12345', debug=False)
    app.logger.info('REST Server has started')


def _dict_default(dic, key, default):
    if key in dic:
        return dic[key]
    else:
        return default


def _format_log(log, monitor_name=""):
    if monitor_name == "":
        resp = '<html><head><title>Monitor Server Log</title></head><body>'
    else:
        resp = '<html><head><title>%s Log</title></head><body>' % monitor_name

    for item in log:
        resp += '<font color="red">%s</font> %s : %s <br>' % (item['time'], item['level'].upper(), item['text'])
    resp += '</body></html>'
    return resp


@app.route('/', methods=['GET'])
def get_default():
    print 'lol'
    return 'lol'


@app.route('/web/<path>', methods=['GET'])
def get_web_file(path):
    if path == "":
        path = "index.html"
    return send_from_directory('files/web/', path)


@app.route('/api/monitors/status.json', methods=['GET'])
def get_monitors_status_json():
    global monitors
    resp = dict()
    resp['status'] = monitors.get_status()
    resp['success'] = True
    return json_obj_response(resp)


@app.route('/api/monitor/<monitor_name>/params.json', methods=['GET'])
def get_monitor_params_json(monitor_name):
    global monitors
    monitor = monitors.get_monitor_by_name(monitor_name)
    if monitor is None:
        app.logger.error('Someone tried to get status from unexisting monitr %s' % monitor_name)
        return json_string_response(
            '{"success": false, "errors": ["monitor with name %s was not found"]}' % monitor_name)

    resp = dict()
    resp['params'] = monitor.params()
    resp['success'] = True

    return json_obj_response(resp)


@app.route('/api/monitor/<monitor_name>/status.json', methods=['GET'])
def get_monitor_status_json(monitor_name):
    global monitors
    monitor = monitors.get_monitor_by_name(monitor_name)
    if monitor is None:
        app.logger.error('Someone tried to get status from unexisting monitr %s' % monitor_name)
        return json_string_response(
            '{"success": false, "errors": ["monitor with name %s was not found"]}' % monitor_name)

    resp = dict()
    resp['status'] = monitor.status()
    resp['success'] = True

    return json_obj_response(resp)


@app.route('/api/monitor/<monitor_name>/log.json', methods=['GET'])
def get_monitor_log_json(monitor_name):
    global monitors

    monitor = monitors.get_monitor_by_name(monitor_name)
    if monitor is None:
        return json_string_response(
            '{"success": false, "errors": ["monitor with name %s was not found"]}' % monitor_name)

    with open('files/logs/%s_log.json' % monitor_name) as f:
        content = f.read()

    content = '{"success": true, "log": [%s]}' % content[0:-2]
    return json_string_response(content)


@app.route('/api/monitor/<monitor_name>', methods=['PUT'])
def add_monitor(monitor_name):
    global monitors
    monitor = monitors.get_monitor_by_name(monitor_name)
    if monitor is not None:
        app.logger.error('Someone tried to create a monitor with a taken name %s' % monitor_name)
        return json_string_response(
            '{"success": false, "errors": ["monitor with the name %s already exists"]}' % monitor_name)

    errors = []

    if 'process_name' not in request.form:
        errors.append('Missing parameter process_name')
    process_name = request.form['process_name']

    if 'init_path' not in request.form:
        errors.append('Missing parameter init_path')
    init_path = request.form['init_path']

    recovery_path = _dict_default(request.form, 'recovery_path', init_path)

    try:
        interval = float(_dict_default(request.form, 'interval', 2))
        if interval < 1:
            errors.append('Parameter interval must be at least 1')
    except ValueError:
        interval = None
        errors.append('Invalid parameter interval')

    try:
        tolerance = float(_dict_default(request.form, 'tolerance', 10))
        if tolerance < 5:
            errors.append('Parameter tolerance must be at least 5')
    except ValueError:
        tolerance = None
        errors.append('Invalid parameter tolerance')

    if len(errors) > 0:
        return json_string_response('{"success": false, "errors": %s}' % str(errors).replace('\'', '"'))

    monitor = ProcessMonitor(process_name,
                             init_path,
                             monitor_name=monitor_name,
                             recovery_path=recovery_path,
                             interval=interval,
                             tolerance=tolerance)

    monitors.add_monitor(monitor)
    return json_string_response('{"success": true}')


@app.route('/api/monitor/<monitor_name>', methods=['PATCH'])
def update_monitor(monitor_name):
    global monitors
    monitor = monitors.get_monitor_by_name(monitor_name)
    if monitor is None:
        return json_string_response(
            '{"success": false, "errors": ["monitor with the name %s not found"]}' % monitor_name)

    if not request.form:
        return json_string_response(
            '{"success": true, "warnings": ["There were no parameters to update"]}')

    errors = []
    if 'interval' in request.form:
        try:
            interval = float(request.form['interval'])
            if interval < 1:
                errors.append('Parameter interval must be at least 1')
        except ValueError:
            interval = None
            errors.append('Invalid parameter interval')
    else:
        interval = None

    if 'tolerance' in request.form:
        try:
            tolerance = float(request.form['tolerance'])
            if tolerance < 5:
                errors.append('Parameter tolerance must be at least 5')
        except ValueError:
            tolerance = None
            errors.append('Invalid parameter tolerance')
    else:
        tolerance = None

    if len(errors) > 0:
        return json_string_response('{"success": false, "errors": %s}' % str(errors).replace('\'', '"'))

    monitor.update_params(interval=interval, tolerance=tolerance)
    return json_string_response('{"success": true}')


@app.route('/api/monitor/<monitor_name>', methods=['DELETE'])
def remove_monitor(monitor_name):
    global monitors
    monitor = monitors.get_monitor_by_name(monitor_name)
    if monitor is None:
        return json_string_response(
            '{"success": false, "errors": ["monitor with the name %s does not exist"]}' % monitor_name)
    if monitor.running:
        monitor.stop()
    monitors.remove_monitor(monitor)
    return json_string_response('{"success": true}')


@app.route('/api/monitor/<monitor_name>/start', methods=['POST'])
def start_monitor(monitor_name):
    global monitors
    monitor = monitors.get_monitor_by_name(monitor_name)
    if monitor is None:
        return json_string_response(
            '{"success": false, "errors": ["monitor with the name %s does not exist"]}' % monitor_name)

    if monitor.running:
        return json_string_response('{"success": false, "errors": ["monitor is already running"]}')

    monitor.start()
    return json_string_response('{"success": true}')


@app.route('/api/monitor/<monitor_name>/stop', methods=['POST'])
def stop_monitor(monitor_name):
    global monitors
    monitor = monitors.get_monitor_by_name(monitor_name)
    if monitor is None:
        return json_string_response(
            '{"success": false, "errors": ["monitor with the name %s does not exist"]}' % monitor_name)

    if not monitor.running:
        return json_string_response('{"success": false, "errors": ["monitor is already stopped"]}')

    monitor.stop()
    return json_string_response('{"success": true}')


@app.route('/api/monitor/<monitor_name>/enable', methods=['POST'])
def enable_monitor(monitor_name):
    global monitors
    monitor = monitors.get_monitor_by_name(monitor_name)
    if monitor is None:
        return json_string_response(
            '{"success": false, "errors": ["monitor with name %s was not found"]}' % monitor_name)

    if monitor.enabled:
        return json_string_response('{"success": false, "errors": ["monitor is already enabled"]}')

    monitor.enable()
    return json_string_response('{"success": true}')


@app.route('/api/monitor/<monitor_name>/disable', methods=['POST'])
def disable_monitor(monitor_name):
    global monitors
    monitor = monitors.get_monitor_by_name(monitor_name)
    if monitor is None:
        return json_string_response(
            '{"success": false, "errors": ["monitor with name %s was not found"]}' % monitor_name)

    if not monitor.enabled:
        return json_string_response('{"success": false, "errors": ["monitor is already disabled"]}')

    monitor.disable()
    return json_string_response('{"success": true}')


start_rest_server()