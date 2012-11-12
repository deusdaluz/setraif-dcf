import flask
import json
import time
import functools
from dcf.models.transacao import Transacao
from dcf.models.transacao import Conta
from flask import render_template
from datetime import datetime
from werkzeug.exceptions import BadRequest

bp = flask.Blueprint("helloworld", __name__)


@bp.route("/")
def index():
    return render_template('index.html')


class CheckException(BadRequest):
    def __init__():


def json_view(view):
    @functools.wraps(view)
    def wrapper():
        return json.dumps(view())
    return wrapper


@bp.route("/checar", methods=["POST"])
@json_view
def checar():
    try:
        data = flask.request.json
        if data is None:
            raise CheckException("Could not parse the json")

        fields = (
            # (name, convert)
            ("idTransaction", unicode),
            ("gpsLat", float),
            ("gpsLong", float),
            ("time", unicode),
            ("date", unicodelambda inp: time.strptime(unicode(inp), "")),
            ("value", float),
            ("idDmtConsum", unicode),
            ("idAccountConsum", unicode)
        )

        clean_data = {}
        for name, convert in fields:
            if not name in data:
                raise CheckException("Field {} is missing".format(name))

            value = None
            try:
                value = convert(data[name])
            except:
                raise CheckException("Could not parse {}".format(name))

            clean_data[name] = value

        try:
            clean_data["datetime"] = datetime.strptime(
                clean_data["time"] + " " + clean_data["date"],
                "%H:%M:%S %d/%m/%Y"
            )
        except:
            raise CheckException("Could not parse time and/or date")

        transacao = Transacao(
            idConta=clean_data["idAccountConsum"],
            idDispositivo=clean_data["idDmtConsum"],
            id=clean_data["idAccountConsum"],
            data=clean_data["datetime"],
            valor=clean_data["value"],
            latitude=clean_data["gpsLat"],
            longitude=clean_data["gpsLong"]
        )

        return json.dumps({
            "idTransaction": "1",
            "isFraud": "false"
        })

    except CheckException, e:
        return json.dumps({
            "erroMsg": e.description
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


@bp.route("/conta")
def conta():
    args = flask.request.args

    if not 'conta' in args:
        return 'Conta nao disponivel'
    
    conta = Conta.get_by_id(args['conta'])
    return render_template('conta_template.html', conta = conta)


@bp.route("/about")
def about():
    return render_template('about.html')


def convert(string_bool):
    if 'False' == string_bool:
        return False
    else:
        return True
