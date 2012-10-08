import flask

bp = flask.Blueprint("helloworld", __name__)


@bp.route("/")
def message():
    return "Hello World!"
