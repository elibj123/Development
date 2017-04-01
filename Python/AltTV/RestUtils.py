import json
from flask import make_response


def json_string_response(json_string):
    response = make_response(json_string)
    response.headers['Content-Type'] = 'application/json'
    return response


def json_obj_response(obj):
    # type: (object) -> str
    response = make_response(json.dumps(obj, ensure_ascii=False))
    response.headers['Content-Type'] = 'application/json'
    return response


def json_success(payload=[], warnings=[]):
    response = {"success": True}
    if payload:
        response[payload.keys()[0]] = payload.values()[0]

    if warnings:
        if not isinstance(warnings, list):
            response["warnings"] = [warnings]
        elif warnings:
            response["warnings"] = warnings

    return json_obj_response(response)


def json_error(errors=[]):
    response = {"success": False}
    if errors:
        if not isinstance(errors, list):
            response["errors"] = [errors]
        else:
            response["errors"] = errors
    return response


def txt_response(string):
    response = make_response(string)
    response.headers['Content-Type'] = 'text/html'
    return response


def dict_default(dic, key, default):
    if key in dic:
        return dic[key]
    else:
        return default