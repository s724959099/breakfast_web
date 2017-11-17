import datetime
from Model.dbModel import db


def db_to_str(cls, relations=None, date_formate="%Y-%m-%d %H:%M"):
    if relations is None:
        relations = []
    for key, val in cls.__dict__.items():
        if val is None:
            cls.__dict__[key] = ""

        if isinstance(val, datetime.datetime):
            cls.__dict__[key] = cls.__dict__[key].strftime(date_formate)
    for relation in relations:
        if isinstance(relation, tuple):
            [relation, fn] = relation
            cls.__dict__[relation] = fn(getattr(cls, relation))

        arg = cls.__dict__.get(relation)
        if arg is None:
            arg = getattr(cls, relation)
        if arg is None:
            pass
        elif isinstance(arg, db.Model):
            setattr(cls, "%s_instance" % relation, BaseJSON(arg))
        elif isinstance(arg, list):
            arr = []
            for item in arg:
                arr.append(BaseJSON(item))
            setattr(cls, "%s_instance" % relation, arr)


class BaseJSON:
    def __new__(cls, arg, relations=None, **kwargs):
        if relations is None:
            relations = []
        if arg is None:
            return
        db_to_str(arg, relations, **kwargs)
        dOutput = arg.__dict__
        # dOutput.pop("CreateDate", None)
        # dOutput.pop("CreateBy", None)
        # dOutput.pop("ModifiedDate", None)
        # dOutput.pop("ModifiedBy", None)
        # dOutput.pop("SoftDelete", None)
        for name in list(dOutput):
            cond1 = name.startswith("_")
            cond2 = name.endswith("_")
            if cond1 or cond2:
                dOutput.pop(name, None)

        for relation in relations:
            dOutput.pop(relation) if not isinstance(relation, tuple) else dOutput.pop(relation[0])
        return dOutput
