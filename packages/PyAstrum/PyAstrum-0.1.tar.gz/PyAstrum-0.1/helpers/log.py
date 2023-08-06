all = ["get_logger", "PyAstrumJSONFormatter"]

import datetime
import json_log_formatter
import logging
import os
import sys

from .config import LOGGING_ENV_VAR


class PyAstrumJSONFormatter(json_log_formatter.JSONFormatter):
    """
    Custom class to override the default behaviour of the JSONFormatter
    """

    def format(self, record):
        """
        JSONFormatter defaults to a casted string. This JSON format can have
        nested dicts
        """
        message = record.msg
        extra = self.extra_from_record(record)
        json_record = self.json_record(message, extra, record)
        mutated_record = self.mutate_json_record(json_record)
        if mutated_record is None:
            mutated_record = json_record
        return self.to_json(mutated_record)

    def json_record(self, message, extra, record):
        """
        Dictionary representation of our messages
        """
        extra['message'] = message
        extra['level'] = record.levelname
        extra['module'] = record.name
        extra['time'] = datetime.datetime.utcnow()
        if record.exc_info:
            extra['exec_info'] = self.formatException(record.exc_info)
        return extra

    def to_json(self, record):
        """
        Converts record dict to a JSON string.
        """
        return self.json_lib.dumps(record, default=_json_object_encoder)


def _json_object_encoder(obj):
    """
    Cast obj to JSON representation
    """
    try:
        return obj.to_json()
    except AttributeError:
        return str(obj)


def get_handler():
    """
    Gets the handler to manage the output of the logger, default: stdout
    """
    handler = logging.StreamHandler(sys.stdout)
    return handler


def get_formatter():
    """
    Formatter definition
    """
    formatter = PyAstrumJSONFormatter
    return formatter()


def get_logging_level():
    """
    Logging level. Defaults to logging.INFO
    """
    return int(os.environ.get(LOGGING_ENV_VAR, logging.INFO))


output_handler = get_handler()
output_handler.setFormatter(get_formatter())


def get_logger(name=None):
    """
    Logger instance
    """
    logger = logging.getLogger(name or __name__)
    logger.addHandler(output_handler)
    logger.setLevel(get_logging_level())
    return logger
