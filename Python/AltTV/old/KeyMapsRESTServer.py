import json
import logging
import os

import flask
from Python.AltTV.RestUtils import *
from flask_cors import CORS

import Python.AltTV.server.LoggerFactory

app = flask.Flask('ProcessMonitor')
app.debug = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

def start_rest_server():
    for handler in Python.AltTV.server.LoggerFactory.get_logger_handler(['files/logs/key_maps_rest_server_log.json']):
        app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.run(host='127.0.0.1', port='12346', debug=False, threaded=True)
    app.logger.info('REST Server has started')


@app.route('/api/keymaps.json', methods=['GET'])
def get_keymaps():

    resp = dict()
    resp['success'] = True
    with open('files/data/keymaps.json','r') as f:
        resp['maps'] = json.loads(f.read())['maps']
    return json_obj_response(resp)


@app.route('/api/keymap/<keymapname>', methods=['POST'])
def activate_keymap(keymapname):
    with open('files/data/keymaps.json', 'r') as f:
        maps = json.loads(f.read())
    path = 'files/data/%s%s' % (maps['dir'], keymapname)
    cmd_line = 'regedit /s %s' % path

    os.system(cmd_line)
    if 'time_to_reboot' in flask.request.form:
        try:
            time = int(flask.request.form['time_to_reboot'])
        finally:
            time = 10

        if time < 10:
            return json_string_response('{"success": true, "warnings": ["No reboot was performed"]}')
    else:
        time = 10

    os.system('shutdown /r /f /t %d' % time)
    return json_string_response('{"success": true, "messages": ["See you on the other side"]}')


start_rest_server()
