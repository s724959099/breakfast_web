from SwaggerWrapper import *
from libs.flask_get import *
from Model.dbModel import *
from Model.ModelJSON import *
from utli.utli import *


def avoid_err(cls):
    for attr in "post get put delete".split():
        if hasattr(cls, attr) and callable(getattr(cls, attr)):
            setattr(cls, attr, try_catch(getattr(cls, attr)))
    return cls


@avoid_err
class UsersResourece(Resource):
    def get(self):
        item = Users.query.filter_by(deleted=False).all()
        from_time = args_get('from_time')
        to_time = args_get('to_time')
        from_time = datetime.datetime.strptime(from_time, '%Y-%m-%d') \
            if from_time is not None else None
        to_time = datetime.datetime.strptime(to_time, '%Y-%m-%d') + datetime.timedelta(days=1) \
            if to_time is not None else None

        result = UsersJSON(item, from_time=from_time, to_time=to_time, arr=True)
        return result

    @json_check_var(['name'])
    def post(self):
        name = json_get('name')
        user = Users(
            name=name,
        )
        db.session.add(user)
        db.session.commit()
        item = UsersJSON(user, arr=True)
        return item


@avoid_err
class UsersIdResourece(Resource):
    def get(self, _id):
        item = Users.query.filter_by(deleted=False, id=_id).scalar()
        result = UsersJSON(item, arr=True)
        from_time = args_get('from_time')
        to_time = args_get('to_time')
        from_time = datetime.datetime.strptime(from_time, '%Y-%m-%d') \
            if from_time is not None else None
        to_time = datetime.datetime.strptime(to_time, '%Y-%m-%d') + datetime.timedelta(days=1) \
            if to_time is not None else None

        result = UsersJSON(item, from_time=from_time, to_time=to_time, arr=True)
        return result

    @json_check_var(['name'])
    def put(self, _id):
        name = json_get('name')
        item = Users.query.filter_by(deleted=False, id=_id).scalar()
        item.name = name
        item.update_date = datetime.datetime.now()
        db.session.commit()

        result = UsersJSON(item, arr=True)
        return result

    def delete(self, _id):
        item = Users.query.filter_by(deleted=True, id=_id).scalar()
        item.deleted = True
        item.update_date = datetime.datetime.now()
        db.session.commit()

        return True


@avoid_err
class UsersIdWorkDatesResourece(Resource):
    def post(self, _id):
        user = Users.query.filter_by(deleted=False, id=_id).scalar()
        if user is None:
            return False
        item = WorkDates(user=user, from_time=work_time_format(datetime.datetime.now()))
        db.session.add(item)
        db.session.commit()

        result = WorkDatesJSON(item)
        return result


@avoid_err
class UsersIdWorkDatesIdResourece(Resource):
    def put(self, _id, _workdates_id):
        item = WorkDates.query.filter_by(user_id=_id, id=_workdates_id).scalar()
        item.to_time = work_time_format(datetime.datetime.now())
        item.update_date = datetime.datetime.now()

        db.session.commit()

        result = WorkDatesJSON(item, deep=False)
        return result


@avoid_err
class WorkDatesResourece(Resource):
    def get(self):
        items = WorkDates.query.filter_by(deleted=False).all()
        result = WorkDatesJSON(item)
        return result


@avoid_err
class WorkDatesIdResourece(Resource):
    def delete(self, _id):
        item = WorkDates.query.filter_by(deleted=True, id=_id).scalar()
        if item is None:
            return False
        item.deleted = True
        item.update_date = datetime.datetime.now()
        db.session.commit()

        return True
