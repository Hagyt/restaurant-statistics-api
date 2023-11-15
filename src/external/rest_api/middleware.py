from functools import wraps

from flask import request


def post_data_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        json_data = request.get_json()
        if json_data is None or json_data == {}:
            raise Exception()
        else:
            return f(json_data, *args, **kwargs)
    return wrapped


def qparams_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        qparams = request.args.to_dict(True)
        if qparams is None or qparams == {}:
            raise Exception()
        else:
            return f(qparams, *args, **kwargs)
    return wrapped