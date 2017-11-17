from flask import *
from libs.functools import *
from contextlib import contextmanager
from Model.dbModel import db


def form_get(var, deafult=None):
    return request.form[var] if request.form.get(var) is not None else deafult


def args_get(var, deafult=None):
    return request.args[var] if request.args.get(var) is not None else deafult


def json_get(var, deafult=None):
    if request.json is None:
        return deafult
    return request.json[var] if request.json.get(var) is not None else deafult


def session_get(var, deafult=None):
    return session[var] if session.get(var) is not None else deafult


def json_check_var(list):
    def not_found(s):
        return "not found json arg:{}".format(s), 520

    def get_func(fn):
        @wraps(fn)
        def get_func_args(*args, **kwargs):
            try:
                if request.json is None:
                    return not_found()
                for l in list:
                    if l not in request.json:
                        return not_found(l)
            except:
                return not_found()

            return fn(*args, **kwargs)

        return get_func_args

    return get_func


def form_check_var(list):
    def not_found(s):
        return return_arg_lack("not found form arg:{}".format(s))

    def not_form():
        return return_format_error("not form type")

    def get_func(fn):
        @wraps(fn)
        def get_func_args(*args, **kwargs):
            try:
                if request.form is None:
                    return not_form()
                for l in list:
                    if l not in request.form:
                        return not_found(l)
            except:
                return not_form()

            return fn(*args, **kwargs)

        return get_func_args

    return get_func


def args_check_var(list):
    def not_found(s):
        return return_arg_lack("not found args arg:{}".format(s))

    def not_args():
        return return_format_error("not args type")

    def get_func(fn):
        @wraps(fn)
        def get_func_args(*args, **kwargs):
            try:
                if request.args is None:
                    return not_args()
                for l in list:
                    if l not in request.args:
                        return not_found(l)
            except:
                return not_args()

            return fn(*args, **kwargs)

        return get_func_args

    return get_func


def try_catch(fn):
    @wraps(fn)
    def inside(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return str(e), 500

    return inside
