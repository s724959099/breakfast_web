from api_urls import api
from rest_api import *
import time
from sys import *

app = Flask(__name__)
app.secret_key = 'edjw8vlsuig2d5djh'
app.register_blueprint(api.blueprint)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

my_version = {
    'version': time.time(),
}


@app.route("/")
def index():
    local = locals()
    local.update(my_version)
    return render_template("page/index.html", **local)


@app.route("/backend")
def backend():
    local = locals()
    local.update(my_version)
    return render_template("page/backend.html", **local)


@app.route("/work-time")
def work_time():
    local = locals()
    local.update(my_version)
    return render_template("page/work_time.html", **local)


@app.route("/employees")
def employees():
    local = locals()
    local.update(my_version)
    return render_template("page/employees.html", **local)


@app.route("/test")
def test():
    local = locals()
    local.update(my_version)
    return render_template("page/test.html", **local)


if __name__ == "__main__":
    app.run(port=2000, debug=True)
