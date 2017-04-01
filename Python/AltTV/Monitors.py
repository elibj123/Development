import json
import logging
import threading
import time

import LoggerFactory
from ProcessMonitor import ProcessMonitor


class MonitorNotFoundError(Exception):
    def __init__(self, monitor_name):
        self.message = 'Monitor with the name %s was not found' % monitor_name


class Monitors(object):
    def __init__(self, persistence_file='files/data/monitors.json'):
        self.logger = LoggerFactory.setup_logger(logger_name='MonitorsRepLogger',
                                                 log_files=['files/logs/monitors_log.json'],
                                                 level=logging.DEBUG)

        self.monitors = list()
        self.persistence_file = persistence_file

        self._load()
        self.running = True

        self.persistence_thread = threading.Thread( target=self._persist )
        self.persistence_thread.start( )

    def __del__(self):
        self.running = False

    def get_monitor_by_name(self, monitor_name):
        for monitor in self.monitors:
            if monitor.monitor_name == monitor_name:
                return monitor
        raise MonitorNotFoundError(monitor_name)

    def get_log(self):
        big_log = list()
        for monitor in self.monitors:
            big_log.extend(monitor.log)
        big_log.sort(key=lambda item: item['ts'])
        return big_log

    def get_status(self):
        big_status = list()
        for monitor in self.monitors:
            big_status.append(monitor.status())

        return big_status

    def add_monitor(self, monitor):
        self.monitors.append(monitor)

    def remove_monitor(self, monitor):
        self.monitors.remove(monitor)

    def _load(self):
        try:
            with open(self.persistence_file, 'r') as fp:
                monitor_json = json.load(fp)
                for monitor in monitor_json['monitors']:
                    self.add_monitor(ProcessMonitor(
                        process_name=monitor['process_name'],
                        monitor_name=monitor['monitor_name'],
                        init_path=monitor['init_path'],
                        recovery_path=monitor['recovery_path'],
                        interval=monitor['interval'],
                        tolerance=monitor['tolerance']
                    ))
            self.logger.info('Loaded monitors from %s' % self.persistence_file)
        except IOError:
            self.logger.error('Failed to load file')

    def _persist(self):
        while self.running:
            time.sleep(5)
            try:
                monitor_obj = [monitor.params() for monitor in self.monitors]
                monitor_dic = dict()
                monitor_dic['monitors'] = monitor_obj
                fp = open(self.persistence_file, 'w')
                json.dump(monitor_dic, fp)
                fp.close()
                self.logger.info('Saved to persistence file')
            except IOError:
                self.logger.error('Failed to save file')
                return
            except Exception as e:
                self.logger.error(e)
                return


monitors = Monitors()
