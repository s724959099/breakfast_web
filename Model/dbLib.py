from Model.dbModel import db
import uuid
import random
import datetime
from libs.flask_get import *
import string


def db_flush():
    try:
        db.session.flush()
        return True, None
    except Exception as e:
        db.session.rollback()
        db.session.remove()
        return False, str(e)


def db_commit():
    try:
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        db.session.remove()
        return False, str(e)


def db_delete_list(datas):
    for data in datas:
        db.session.delete(data)


def getuuid():
    return str(uuid.uuid1())


def getOrderNumber(start="",Length=5,end=""):
    a = datetime.datetime.utcnow()
    a = a + datetime.timedelta(hours=8)
    NewOrderNumberRandom = ''.join(random.choice(string.digits) for _ in range(Length))
    m = a.month
    if len(str(m)) == 1:
        m = str(m).zfill(2)
    d = a.day
    if len(str(d)) == 1:
        d = str(d).zfill(2)
    h = a.hour
    if len(str(h)) == 1:
        h = str(h).zfill(2)
    NewOrderNumber = str(a.year)[2:] + str(m) + str(d) + str(h) + "-" + NewOrderNumberRandom
    return start+NewOrderNumber+end

def random_str(length=8):
    l = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
        'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    ]

    getId = ''.join(random.choice(l) for _ in range(length))
    return getId


def data_update_db(cls, datas, fn=db_commit):
    """
    get datas which is [{"name":var,"value":var},....]
    :return:
    """
    if cls is None:
        return False, "Model not found"
    UserId = session_get("UserId", "SYSTEM")
    for data in datas:
        if data["value"] != "":
            setattr(cls, data["name"], data["value"])

    # modify then need to record
    cls.ModifiedDate = datetime.datetime.now()
    cls.ModifiedBy = UserId
    return fn()


def dict_to_array(array, d):
    """
    array=[{"name":var, "value":var}...]
    :param d:dict
    :return: array
    """
    datas = []
    for key, value in d.items():
        datas.append({
            "name": key,
            "value": value
        })
    array.extend(datas)


def datas_add_order(datas, *args):
    """
    datas add name:1,name:2... order
    :param datas:
    :param name:
    :return:
    """
    for index, data in enumerate(datas):
        i = index + 1
        obj = data
        for arg in args:
            obj[arg] = i
        datas[index] = obj


def dict_insert_db(cls, cls_dict, other_dict={}, fn=db_commit):
    """
    get datas which is [{"name":var,"value":var},....]
    :return:
    """
    if not cls_dict:
        suc, msg = fn()
        return suc, msg, None
    UserId = session_get("UserId", "SYSTEM")
    other_dict["CreateBy"] = UserId
    cls_dict.update(other_dict)

    if cls is None:
        return False, "Model not found"

    obj = cls(**cls_dict)
    db.session.add(obj)

    suc, msg = fn()
    return suc, msg, obj


def dict_insert_db_list(cls, datas, other_dict={}, fn=db_commit):
    """
    get datas which is [{"name":var,"value":var},....]
    :return:
    """
    if not datas:
        suc, msg = fn()
        return suc, msg, None

    UserId = session_get("UserId", "SYSTEM")
    other_dict["CreateBy"] = UserId

    if cls is None:
        return False, "Model not found"
    for cls_dict in datas:
        cls_dict.update(other_dict)
        obj = cls(**cls_dict)
        db.session.add(obj)

    suc, msg = fn()
    return suc, msg, obj


def dict_update_db(cls, cls_dict, fn=db_commit):
    """
    get datas which is [{"name":var,"value":var},....]
    :return:
    """
    if cls is None:
        return False, "Model not found"
    UserId = session_get("UserId", "SYSTEM")
    for key, value in cls_dict.items():
        if value != "":
            setattr(cls, key, value)

    # modify then need to record
    cls.ModifiedDate = datetime.datetime.now()
    cls.ModifiedBy = UserId
    return fn()


def data_insert_db(cls, datas, other_dict={}, fn=db_commit):
    """
    get datas which is [{"name":var,"value":var},....]
    :return:
    """
    UserId = session_get("UserId", "SYSTEM")
    other_dict["CreateBy"] = UserId
    dict_to_array(datas, other_dict)
    cls_dict = {}
    if cls is None:
        return False, "Model not found"

    for data in datas:
        cls_dict[data["name"]] = data["value"]
    obj = cls(**cls_dict)
    db.session.add(obj)

    suc, msg = fn()
    return suc, msg, obj


def data_insert_db_list(cls, datas, other_dict={}, fn=db_commit):
    """
    get datas which is [{"name":var,"value":var},....]
    :return:
    """
    UserId = session_get("UserId", "SYSTEM")
    other_dict["CreateBy"] = UserId
    obj_list = []
    if cls is None:
        return False, "Model not found"

    for data in datas:
        cls_dict = {}
        dict_to_array(data, other_dict)
        for d in data:
            cls_dict[d["name"]] = d["value"]
        obj = cls(**cls_dict)
        db.session.add(obj)
        obj_list.append(obj_list)

    suc, msg = fn()
    return suc, msg, obj_list


def str_to_date(s):
    '''
    formate:2015/07/01
    str to date format
    '''
    d = datetime.datetime.strptime(s, '%Y/%m/%d')
    return d
