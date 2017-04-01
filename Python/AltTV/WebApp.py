from flask import Blueprint, send_from_directory

web_app_handler = Blueprint('WebHandler', __name__)


@web_app_handler.route('/app/<file_name>', methods=['GET'])
def get_path(file_name):
    return send_from_directory('files/web/', file_name)


@web_app_handler.route('/app/<subdir>/<file_name>', methods=['GET'])
def get_sub_path_file(subdir, file_name):
    return send_from_directory('files/web/%s/' % subdir, file_name )
