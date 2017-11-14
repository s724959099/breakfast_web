def return_exist(arg):
    return {
        "exist": arg,
        "code": 200
    }


def return_format_error(msg):
    return {
        "msg": msg,
        "code": 900,
    }


def return_arg_lack(msg):
    return {
        "msg": msg,
        "code": 901
    }


def return_msg(msg):
    return {
        "msg": msg,
        "code": 200
    }


def return_json(js):
    js["code"] = 200
    return js


def return_db_fail(msg):
    return {
        "msg": msg,
        "code": 902
    }

def return_unknown(msg):
    return {
        "msg": msg,
        "code": 904
    }

