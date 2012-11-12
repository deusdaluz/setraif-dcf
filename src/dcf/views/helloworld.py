import flask
import json
from dcf.models.transacao import Transacao
from flask import render_template
from datetime import datetime
from werkzeug.exceptions import BadRequest

bp = flask.Blueprint("helloworld", __name__)


@bp.route("/")
def index():
    return render_template('index.html')


@bp.route("/checar", methods=["POST"])
def message():
    if flask.request.json is None:
        raise BadRequest()
    return json.dumps({
        "idTransaction": "1",
        "isFraud": "false"
    })


@bp.route("/relatorio")
def relatorio():
    transacoes = Transacao.query().fetch()
    args = flask.request.args

    query = Transacao.query()
    for key in args:
        if args[key] != '':
            if key == 'ehFraude':
                query = query.filter(Transacao.ehFraude == convert(args['ehFraude']))
            elif key == 'dataInic':
                query = query.filter(Transacao.data >= datetime.strptime(args[key], '%Y-%m-%d'))
            elif key == 'dataFim':
                query =  query = query.filter(Transacao.data < datetime.strptime(args[key], '%Y-%m-%d'))
            else:
                query = query.filter(getattr(Transacao,key) == args[key])

            transacoes = query.fetch()

    return render_template('list_transacoes.html', transacoes = transacoes , args = args)


@bp.route("/about")
def about():
    return render_template('about.html')


def convert(string_bool):
    if 'False' == string_bool:
        return False
    else:
        return True
