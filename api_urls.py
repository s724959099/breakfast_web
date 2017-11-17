from rest_api import *
from flask_cors import CORS

restapi = Blueprint('api', __name__)
CORS(restapi)
api = Api(
    restapi, api_version='1.0', title="REST API",
    description=""
)


@restapi.teardown_request
def teardown_request(res):
    db.session.remove()


api.add_resource(UsersResourece, '/api/users')
api.add_resource(UsersIdResourece, '/api/users/<_id>')
api.add_resource(UsersIdWorkDatesResourece, '/api/users/<_id>/workdates')
api.add_resource(UsersIdWorkDatesIdResourece, '/api/users/<_id>/workdates/<_workdates_id>')

api.add_resource(WorkDatesResourece, '/api/workdates')
api.add_resource(WorkDatesIdResourece, '/api/workdates/<_id>')
