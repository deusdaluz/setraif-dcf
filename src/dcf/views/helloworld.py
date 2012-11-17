import flask
import json
import time
import functools
from dcf.models.transacao import Transacao
from dcf.models.transacao import Conta
import dcf.checks as checks
from flask import render_template
from datetime import datetime
from werkzeug.exceptions import BadRequest
import google.appengine.ext.ndb as ndb

bp = flask.Blueprint("helloworld", __name__)


@bp.route("/")
def index():
    return render_template('index.html')


class CheckException(BadRequest):
    pass

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
            ("date", unicode),
            ("value", float),
            ("idDmtConsum", unicode),
            ("idAccountConsum", unicode)
        )

        clean_data = {}
        import logging
        for name, convert in fields:
            if not name in data:
                raise CheckException("Field \"{}\" is missing".format(name))

            value = None
            try:
                value = convert(data[name])
            except:
                raise CheckException("Could not parse \"{}\"".format(name))

            clean_data[name] = value

        try:
            clean_data["datetime"] = datetime.strptime(
                clean_data["time"] + " " + clean_data["date"],
                "%H:%M:%S %d/%m/%Y"
            )
        except:
            raise CheckException("Could not parse time and/or date")

        #@ndb.transactional(xg=True)
        def check_and_save():
            if Transacao.get_by_id(clean_data["idTransaction"]):
                raise CheckException("This transaction already exists")

            conta = Conta.get_by_id(clean_data["idAccountConsum"])
            if not conta:
                raise CheckException("Invalid account")
            conta_old_values = conta.to_dict()

            transacao = Transacao(
                idConta=clean_data["idAccountConsum"],
                idDispositivo=clean_data["idDmtConsum"],
                id=clean_data["idTransaction"],
                data=clean_data["datetime"],
                valor=clean_data["value"],
                latitude=clean_data["gpsLat"],
                longitude=clean_data["gpsLong"]
            )
            transacao.ehFraude = checks.is_fraud(transacao, conta)
            checks.learn(transacao, conta)
            if conta.to_dict() != conta_old_values:
                conta.put()
            transacao.put()

            return transacao

        transacao = check_and_save()

        return {
            "idTransaction": transacao.id,
            "isFraud": "true" if transacao.ehFraude else "false"
        }

    except CheckException, e:
        return {
            "erroMsg": e.description
        }

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
            elif key == 'posicao':
                posicao = args['posicao'].split('k')
                if len(posicao) == 3:
                    query = query.filter(Transacao.longitude >= float(posicao[0]))
                    query = query.filter(Transacao.latitude >= float(posicao[1]))
                    query = query.filter(Transacao.longitude <= float(posicao[2]))            
                    query = query.filter(Transacao.latitude <= float(posicao[3]))

            else:
                query = query.filter(getattr(Transacao,key) == args[key])

    
    transacoes = query.fetch()

    if 'posicao' in args and args['posicao'] != '':
         posicao = args['posicao'].split('k')
         transacoes = [x for x in transacoes if x.latitude >= float(posicao[0]) and x.longitude >= float(posicao[1]) and x.latitude <= float(posicao[2]) and x.longitude <= float(posicao[3])]


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
