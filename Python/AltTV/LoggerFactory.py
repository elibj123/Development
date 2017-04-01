import logging


def setup_logger(logger_name, log_files, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter(  "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s")
    json_formatter = logging.Formatter('{"time": "%(asctime)s", "message": "%(message)s", "level": "%(levelname)s",'
                                       ' "name": "%(name)s"},')

    if not isinstance(log_files, list):
        log_files = [log_files]
    for log_file in log_files:
        file_handler = logging.FileHandler(log_file, mode='w+')
        file_handler.setFormatter(json_formatter)
        l.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(stream_handler)

    return l


def get_logger_handler(log_files, level=logging.INFO):
    json_formatter = logging.Formatter('{"time": "%(asctime)s", "message": "%(message)s", "level": "%(levelname)s",'
                                       ' "name": "%(name)s"},')

    for log_file in log_files:
        file_handler = logging.FileHandler(log_file, mode='w+')
        file_handler.setFormatter(json_formatter)
        file_handler.setLevel(level)
        yield file_handler


