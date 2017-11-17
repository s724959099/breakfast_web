from SwaggerWrapper import *
from libs.flask_get import *
from Model.dbModel import *
from Model.ModelJSON import *


def avoid_err(cls):
    for attr in "post get put delete".split():
        if hasattr(cls, attr) and callable(getattr(cls, attr)):
            setattr(cls, attr, try_catch(getattr(cls, attr)))
    return cls


@avoid_err
class UsersResourece(Resource):
    def get(self):
        items = Users.query.filter_by(deleted=False).all()
        result = []
        for item in items:
            item = BaseJSON(item, [
                ('work_dates', lambda q: q.filter_by(deleted=False).all())
            ])
            result.append(item)
        return result

    @json_check_var(['name'])
    def post(self):
        name = json_get('name')
        user = Users(
            name=name,
        )
        db.session.add(user)
        db.session.commit()
        user = Users.query.get(user.id)
        item = BaseJSON(user, [
            ('work_dates', lambda q: q.filter_by(deleted=False).all())
        ])
        return item


@avoid_err
class UsersIdResourece(Resource):
    def get(self, _id):
        item = Users.query.filter_by(deleted=False, id=_id).scalar()
        result = BaseJSON(item, [
            ('work_dates', lambda q: q.filter_by(deleted=False).all())
        ])
        return result

    @json_check_var(['name'])
    def put(self, _id):
        name = json_get('name')
        item = Users.query.filter_by(deleted=False, id=_id).scalar()
        item.name = name
        db.session.commit()

        item = Users.query.filter_by(deleted=False, id=_id).scalar()
        result = BaseJSON(item, [
            ('work_dates', lambda q: q.filter_by(deleted=False).all())
        ])
        return result

    def delete(self, _id):
        item = Users.query.filter_by(deleted=True, id=_id).scalar()
        if item is None:
            return False
        item.deleted = True
        db.session.commit()

        return True


@avoid_err
class UsersIdWorkDatesResourece(Resource):
    def post(self, _id):
        user = Users.query.filter_by(deleted=False, id=_id).scalar()
        if user is None:
            return False
        item = WorkDates(user=user)
        db.session.add(item)
        db.session.commit()

        item = WorkDates.query.filter_by(deleted=False, id=item.id).scalar()
        if item is None:
            return False
        result = BaseJSON(item, ['user'])
        return result


@avoid_err
class WorkDatesResourece(Resource):
    def get(self):
        items = WorkDates.query.filter_by(deleted=False).all()
        result = []
        for item in items:
            item = BaseJSON(item, ['user'])
            result.append(item)
        return result


@avoid_err
class WorkDatesIdResourece(Resource):
    def delete(self, _id):
        item = WorkDates.query.filter_by(deleted=True, id=_id).scalar()
        if item is None:
            return False
        item.deleted = True
        db.session.commit()

        return True
