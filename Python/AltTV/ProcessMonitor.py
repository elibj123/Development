import csv
import logging
import subprocess
import threading
import time
import LoggerFactory


def time_str():
    return time.strftime('%d/%m/%Y %H:%M:%S')


class ProcessMonitor(object):

    task_list_cmd_template = 'tasklist.exe /v /fo csv /fi "IMAGENAME eq %s"'
    task_list_none_str = 'INFO: No tasks are running which match the specified criteria.'
    task_kill_cmd_template = 'taskkill.exe /pid %s /f'

    def __init__(self, process_name, init_path, monitor_name="", recovery_path="", interval=2, tolerance=20):

        self.logger = LoggerFactory.setup_logger(monitor_name + 'Logger',
                                                 log_files=['files/logs/%s_log.json' % monitor_name],
                                                 level=logging.DEBUG)

        self.process_name = process_name
        self.cmd_line = ProcessMonitor.task_list_cmd_template % self.process_name

        if monitor_name == "":
            self.monitor_name = process_name
        else:
            self.monitor_name = monitor_name

        self.init_start_path = init_path

        if recovery_path == "":
            self.recovery_start_path = init_path
        else:
            self.recovery_start_path = recovery_path

        self.monitoring_interval = interval
        self.non_responding_tolerance = tolerance

        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = False
        self.running = False
        self.monitoring_thread.start()

        self.enabled = True
        self.first_start = 1
        self.current_process_status = ''
        self.last_process_check = ''
        self.last_up_time = 0
        self.last_kill_time = 0
        self.last_start_time = 0
        self.last_unresponsive_time = 0

        self.logger.info('New monitor created: %s' % monitor_name)

    def __del__(self):
        self.logger.info('Monitor was shutdown')

    def update_params(self, interval=None, tolerance=None):
        if interval is not None:
            self.monitoring_interval = interval
            self.logger.info('Updated parameter interval to %f' % interval)

        if tolerance is not None:
            self.non_responding_tolerance = tolerance
            self.logger.info('Updated parameter tolerance to %f' % tolerance)

    def start(self):
        if not self.running:
            self.running = True
            self.logger.info('Started monitoring process %s' % self.process_name)

    def stop(self):
        if self.running:
            self.running = False
            self.logger.info('Stopped monitoring process %s' % self.process_name)

    def enable(self):
        if not self.enabled:
            self.enabled = True
            self.logger.info('Action is enabled')

    def disable(self):
        if self.enabled:
            self.enabled = False
            self.logger.info('Action is disabled')

    def params(self):
        return {
            'monitor_name': self.monitor_name,
            'process_name': self.process_name,
            'init_path': self.init_start_path,
            'recovery_path': self.recovery_start_path,
            'interval': self.monitoring_interval,
            'tolerance': self.non_responding_tolerance
        }

    def status(self):
        return {
            'monitorName': self.monitor_name,
            'monitorRunning': self.running,
            'processName': self.process_name,
            'monitorEnabled': self.enabled,
            'status': "None" if self.current_process_status == "" else self.current_process_status,
            'statusLastUpdate': time_str() if self.current_process_status == "" else self.last_process_check}

    def _get_process_status(self):
        self.last_process_check = time_str()
        try:
            p_task_list = subprocess.Popen(self.cmd_line, stdout=subprocess.PIPE, universal_newlines=True)
            p_task_list.wait()
            csv_reader = csv.DictReader(p_task_list.stdout)
            if csv_reader.fieldnames[0] == ProcessMonitor.task_list_none_str:
                return 'Down'
            process_info = csv_reader.next()
            self.process_id = process_info['PID']
            return process_info['Status']
        except Exception as e:
            self.logger.error('Unable to acquire process status: %s' % e.message)
            return 'Error'

    def _monitoring_loop(self):
        while True:
            if self.running:
                try:
                    process_status = self._get_process_status()
                    self._handle_process_status(process_status)
                except Exception as e:
                    self.logger.error(e)
                time.sleep(self.monitoring_interval)

    def _handle_process_status(self, process_status):
        process_status_changed = not process_status == self.current_process_status
        if process_status == 'Running' or process_status == 'Unknown':
            if process_status_changed:
                self.last_up_time = time.time()
                self.logger.info('Current status is %s (%.0f secs)' % (process_status, time.time() - self.last_up_time))
            self.first_start = 0
            self.last_start_time = 0
            self.last_kill_time = 0
        elif process_status == 'Down':
            if process_status_changed:
                self.logger.info('Current status is Down')
            if self.enabled:
                self._start_process()
        elif process_status == 'Not Responding':
            if process_status_changed:
                self.last_unresponsive_time = time.time()
                self.logger.info('Current status is Not Responding (%.0f secs)' % (time.time() - self.last_unresponsive_time))

            if self.enabled and (time.time() - self.last_unresponsive_time) > self.non_responding_tolerance:
                self._kill_process()
        elif not process_status == 'Error':
            raise Exception('Unknown string for process status: %s' % process_status)
        self.current_process_status = process_status

    def _start_process(self):
        if self.first_start == 1:
            path = self.init_start_path
        else:
            path = self.recovery_start_path

        if (time.time() - self.last_start_time) > 30:
            self.logger.info('Starting up process')
            self.last_start_time = time.time()
            subprocess.Popen(path, stdout=subprocess.PIPE)

    def _kill_process(self):
        if (time.time() - self.last_kill_time) > 30:
            self.logger.info('Killing process')
            self.last_kill_time = time.time()
            subprocess.Popen(ProcessMonitor.task_kill_cmd_template % self.process_id, stdout=subprocess.PIPE)

    def log_path(self):
        return 'files/logs/%s_log.json' % self.monitor_name
