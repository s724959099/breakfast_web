import datetime
from libs.azureAPI import *

def db_to_str(cls, date_formate="%Y/%m/%d"):
    for key, val in cls.__dict__.items():
        if val is None:
            cls.__dict__[key] = ""

        if isinstance(val, datetime.datetime):
            cls.__dict__[key] = cls.__dict__[key].strftime(date_formate)


class baseJSON:
    def __new__(cls, arg):
        if arg is None:
            return
        db_to_str(arg)
        dOutput = arg.__dict__
        dOutput.pop("CreateDate", None)
        dOutput.pop("CreateBy", None)
        dOutput.pop("ModifiedDate", None)
        dOutput.pop("ModifiedBy", None)
        dOutput.pop("SoftDelete", None)
        for name in list(dOutput):
            cond1 = name.startswith("_")
            cond2 = name.endswith("_")
            if cond1 or cond2:
                dOutput.pop(name, None)
        return dOutput