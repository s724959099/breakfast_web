# from SwaggerWrapper import *
from libs.flask_get import *

from Model.dbModel import *
from Model.ModelJSON import *

# import time

user = Users.query.first()
w = WorkDates.query.filter_by(user=user).first()
# AA = BaseJSON(w, ['user'])
AA = BaseJSON(user, [
    ('work_dates', lambda q: q.filter_by(deleted=False).first())
])
print("done")
