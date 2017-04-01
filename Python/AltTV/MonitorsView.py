from flask import Blueprint
from RestUtils import *
import logging
from Monitors import monitors
from Decorators import *
monitors_view_handler = Blueprint('MonitorsViewHandler', __name__)


@monitors_view_handler.route('/api/monitors/status.json', methods=['GET'])
def get_monitors_status_json():
    global monitors
    try:
        return json_success({"status": monitors.get_status()})
    except Exception as e:
        logging.getLogger('RestServerLogger').error(e.message)
        return json_error(e.message)


@monitors_view_handler.route('/api/monitor/<monitor_name>/params.json', methods=['GET'])
@verify_monitor_exists
def get_monitor_params_json(monitor):
    return json_success({"params": monitor.params()})


@monitors_view_handler.route('/api/monitor/<monitor_name>/status.json', methods=['GET'])
@verify_monitor_exists
def get_monitor_status_json(monitor):
    return json_success({"status": monitor.status()})


@monitors_view_handler.route('/api/monitor/<monitor_name>/log.json', methods=['GET'])
@verify_monitor_exists
def get_monitor_log_json(monitor):
    with open(monitor.log_path()) as f:
        content = f.read()

    content = '{"success": true, "log": [%s]}' % content[0:-2]
    return json_string_response(content)
