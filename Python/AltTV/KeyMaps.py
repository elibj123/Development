from flask import Blueprint, request
from RestUtils import *
import json
import os

key_maps_handler = Blueprint('KeyMapsHandler', __name__)


@key_maps_handler.route('/api/keymaps/keymaps.json', methods=['GET'])
def get_keymaps():
    try:
        with open('files/data/keymaps.json', 'r') as f:
            maps = json.loads(f.read())['maps']
    except IOError as e:
        return json_error(e.message)
    return json_success({"maps": maps})


@key_maps_handler.route('/api/keymaps/<map_name>', methods=['POST'])
def activate_keymap(map_name):
    with open('files/data/keymaps.json', 'r') as f:
        maps = json.loads(f.read())
    path = 'files/data/%s%s' % (maps['dir'], map_name)
    cmd_line = 'regedit /s %s' % path

    os.system(cmd_line)
    if 'time_to_reboot' in request.form:
        try:
            time = int(request.form['time_to_reboot'])
        except Exception:
            time = 10

        if time < 10:
            return json_success(warnings="No reboot was performed")
    else:
        time = 10

    os.system('shutdown /r /f /t %d' % time)
    return json_success({"messages": "See you on the other side"})
