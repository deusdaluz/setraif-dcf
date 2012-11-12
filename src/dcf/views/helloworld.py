import flask
import json
from dcf.models.transacao import Transacao
from dcf.models.transacao import Conta
from flask import render_template
from datetime import datetime

bp = flask.Blueprint("helloworld", __name__)


@bp.route("/")
def message():
    return json.dumps({
        "idTransaction":"1",
        "isFraud":"false" if "legitima" in flask.request.args else "true"
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