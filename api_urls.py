from rest_api import *
from flask_cors import CORS

restapi = Blueprint('api', __name__)
CORS(restapi)
api = Api(
    restapi, api_version='1.0', title="Cloudesign REST API",
    description=""
)