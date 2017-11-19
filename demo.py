# from SwaggerWrapper import *
from libs.flask_get import *

from Model.dbModel import *
from Model.ModelJSON import *

# import time

A_U = Users.query.first()

from_time = '2017-11-16'
to_time = '2017-11-17'
from_time = datetime.datetime.strptime(from_time, '%Y-%m-%d')
to_time = datetime.datetime.strptime(to_time, '%Y-%m-%d') + datetime.timedelta(days=1)

A_W = WorkDates.query.filter_by(user=A_U).filter(WorkDates.from_time > from_time, WorkDates.to_time < to_time).all()

# # AA = BaseJSON(w, ['user'])
# user.test13 = 'gggc'
# AA = BaseJSON(user, [
#     ('work_dates', lambda q: q.filter_by(deleted=False).first())
# ])

print("done")
