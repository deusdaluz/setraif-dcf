import flask
import json

bp = flask.Blueprint("helloworld", __name__)


@bp.route("/")
def message():
    return json.dumps({
        "idTransaction":"1",
        "isFraud":"false" if "legitima" in flask.request.args else "true"
    })
