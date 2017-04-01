from Decorators import *
from flask import Blueprint, request
import ProcessMonitor
from Monitors import monitors
from RestUtils import *

monitors_control_handler = Blueprint('MonitorsControlHandler', __name__)


@monitors_control_handler.route('/api/monitor/<monitor_name>', methods=['PUT'])
@verify_monitor_not_exists
def add_monitor(monitor_name):
    errors = []

    if 'process_name' not in request.form:
        errors.append('Missing parameter process_name')
    process_name = request.form['process_name']

    if 'init_path' not in request.form:
        errors.append('Missing parameter init_path')
    init_path = request.form['init_path']

    recovery_path = dict_default(request.form, 'recovery_path', init_path)

    try:
        interval = float(dict_default(request.form, 'interval', 2))
        if interval < 1:
            errors.append('Parameter interval must be at least 1')
    except ValueError:
        interval = None
        errors.append('Invalid parameter interval')

    try:
        tolerance = float(dict_default(request.form, 'tolerance', 10))
        if tolerance < 5:
            errors.append('Parameter tolerance must be at least 5')
    except ValueError:
        tolerance = None
        errors.append('Invalid parameter tolerance')

    if len(errors) > 0:
        return json_error(errors)

    monitor = ProcessMonitor.ProcessMonitor(process_name,
                                            init_path,
                                            monitor_name=monitor_name,
                                            recovery_path=recovery_path,
                                            interval=interval,
                                            tolerance=tolerance)

    monitors.add_monitor(monitor)
    return json_success()


# noinspection PyUnresolvedReferences
@monitors_control_handler.route('/api/monitor/<monitor_name>', methods=['PATCH'])
@verify_monitor_exists
def update_monitor(monitor):
    if not request.form:
        return {"success": True, "warnings": ["There were no parameters to update"]}

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
        return json_error(errors)

    monitor.update_params(interval=interval, tolerance=tolerance)
    return json_success()


# noinspection PyUnresolvedReferences
@monitors_control_handler.route('/api/monitor/<monitor_name>', methods=['DELETE'])
@verify_monitor_exists
def remove_monitor(monitor):
    if monitor.running:
        monitor.stop()
    monitors.remove_monitor(monitor)
    return json_success()


# noinspection PyUnresolvedReferences
@monitors_control_handler.route('/api/monitor/<monitor_name>/start', methods=['POST'])
@verify_monitor_exists
def start_monitor(monitor):
    if monitor.running:
        return json_error("monitor is already running")

    monitor.start()
    return json_success()


# noinspection PyUnresolvedReferences
@monitors_control_handler.route('/api/monitor/<monitor_name>/stop', methods=['POST'])
@verify_monitor_exists
def stop_monitor(monitor):
    if not monitor.running:
        return json_error("monitor is already stopped")

    monitor.stop()
    return json_success()


# noinspection PyUnresolvedReferences
@monitors_control_handler.route('/api/monitor/<monitor_name>/enable', methods=['POST'])
@verify_monitor_exists
def enable_monitor(monitor):
    if monitor.enabled:
        return json_error("monitor is already enabled")

    monitor.enable()
    return json_success()


# noinspection PyUnresolvedReferences
@monitors_control_handler.route('/api/monitor/<monitor_name>/disable', methods=['POST'])
@verify_monitor_exists
def disable_monitor(monitor):
    if not monitor.enabled:
        return json_error("monitor is already disabled")

    monitor.disable()
    return json_success()
