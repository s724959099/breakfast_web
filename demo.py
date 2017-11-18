# from SwaggerWrapper import *
from libs.flask_get import *

from Model.dbModel import *
from Model.ModelJSON import *

# import time

user = Users.query.first()
w = WorkDates.query.filter_by(user=user).first()
# # AA = BaseJSON(w, ['user'])
# user.test13 = 'gggc'
# AA = BaseJSON(user, [
#     ('work_dates', lambda q: q.filter_by(deleted=False).first())
# ])

AAB = UsersJSON(user, arr=True)
print("user called")
AAA = WorkDatesJSON(w, arr=True)
AAB.pop("_sa_instance_state")
AAA.pop("_sa_instance_state")
print(AAB)
print(AAA)
print("done")
