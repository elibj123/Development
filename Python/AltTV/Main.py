from flask import Flask
from flask_cors import CORS
import Monitors
import LoggerFactory
import logging
import MonitorsControl
import MonitorsView
import WebApp
import KeyMaps

server = Flask(__name__)
LoggerFactory.setup_logger(logger_name='RestServerLogger', level='DEBUG', log_files=['files/logs/rest_server_log.json'])
#server.debug = False
server.register_blueprint(MonitorsControl.monitors_control_handler)
server.register_blueprint(MonitorsView.monitors_view_handler)
server.register_blueprint(WebApp.web_app_handler)
server.register_blueprint(KeyMaps.key_maps_handler)

cors = CORS(server, resources={r"/api/*": {"origins": "*"}})

for handler in LoggerFactory.get_logger_handler(['files/logs/rest_server_log.json']):
    server.logger.addHandler(handler)
server.logger.setLevel(logging.DEBUG)
server.run(host='127.0.0.1', port=8080, debug=False, threaded=True)
server.logger.info('REST Server has started')


