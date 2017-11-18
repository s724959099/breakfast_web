import datetime
from Model.dbModel import *
import copy


def db_to_str(cls, relations=None, date_formate="%Y-%m-%d %H:%M"):
    if relations is None:
        relations = []
    for key, val in cls.__dict__.items():
        if val is None:
            cls.__dict__[key] = ""
        if isinstance(val, db.Model):
            cls.__dict__[key] = BaseJSON(val)

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
        # 不用再判斷了
        if isinstance(arg, dict):
            return arg
        if relations is None:
            relations = []
        if arg is None:
            return
        if isinstance(arg, list):
            # 不用再判斷了
            if isinstance(arg[0], dict):
                return arg
            result = []
            for a in arg:
                result.append(BaseJSON(a))
            return result

        db_to_str(arg, relations, **kwargs)
        # avoid _sa_instance_state bug
        dOutput = copy.deepcopy(arg.__dict__)

        for name in list(dOutput):
            cond1 = name.startswith("_")
            cond2 = name.endswith("_")
            if cond1 or cond2:
                dOutput.pop(name, None)

        for relation in relations:
            dOutput.pop(relation) if not isinstance(relation, tuple) else dOutput.pop(relation[0])
        return dOutput


def check_arr_instance(kwargs, instance):
    if kwargs.get('arr'):
        return instance.all()
    else:
        return instance.first()


class BaseModelJSON:
    def __new__(cls, item, *args, **kwargs):
        if isinstance(item, list):
            result = []
            for i in item:
                result.append(cls(i, *args, **kwargs))
            return result
        else:
            result = cls.to_json(cls, item, *args, **kwargs)
            return result

    def to_json(self, item, *args, **kwargs):
        pass


class UsersJSON(BaseModelJSON):
    def to_json(self, item, *args, **kwargs):
        if kwargs.get('deep', True):
            item.work_dates_instance = check_arr_instance(
                kwargs,
                item.work_dates.filter_by(deleted=False).order_by(WorkDates.create_date.desc())
            )
            item.work_dates_instance = WorkDatesJSON(item.work_dates_instance, deep=False)

        result = BaseJSON(item)
        return result


class WorkDatesJSON(BaseModelJSON):
    def to_json(self, item, *args, **kwargs):
        if kwargs.get('deep', True):
            UsersJSON(item.user, deep=False)
        return BaseJSON(item)
