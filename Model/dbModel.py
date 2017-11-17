import datetime
import uuid
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import aliased

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "sqlite:///sqlite3.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def get_uuid():
    return str(uuid.uuid1())


class Users(db.Model):
    id = db.Column(db.String, primary_key=True, default=get_uuid)
    name = db.Column(db.String)
    create_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
    update_date = db.Column(db.DateTime(timezone=True))
    delete_date = db.Column(db.DateTime(timezone=True))
    deleted = db.Column(db.Boolean, nullable=False, default=False)


class WorkDates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_time = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
    to_time = db.Column(db.DateTime(timezone=True))
    notes = db.Column(db.Text)
    create_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
    update_date = db.Column(db.DateTime(timezone=True))
    delete_date = db.Column(db.DateTime(timezone=True))
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('work_dates', lazy='dynamic'))


if __name__ == '__main__':
    manager.run()
