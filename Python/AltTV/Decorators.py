import logging
from functools import wraps

from Monitors import monitors, MonitorNotFoundError

from RestUtils import json_error


def verify_monitor_exists(func):
    @wraps(func)
    def verified_func(monitor_name):
        try:
            monitor = monitors.get_monitor_by_name(monitor_name)
        except MonitorNotFoundError as e:
            logging.getLogger('RestServerLogger').error(
                'Someone tried to access from non-existing monitor %s' % monitor_name)
            return json_error(e.message)
        except Exception as e:
            logging.getLogger('RestServerLogger').error(e.message)
            return json_error(e.message)
        return func(monitor)
    return verified_func


def verify_monitor_not_exists(func):
    @wraps(func)
    def verified_func(monitor_name):
        try:
            monitor = monitors.get_monitor_by_name(monitor_name)
            if monitor is not None:
                error = 'Someone tried to add an existing monitor %s' % monitor_name
                logging.getLogger('RestServerLogger').error(error)
                return json_error(error)
        except MonitorNotFoundError as e:
            pass
        except Exception as e:
            logging.getLogger('RestServerLogger').error(e.message)
            return json_error(e.message)
        return func(monitor_name)
    return verified_func