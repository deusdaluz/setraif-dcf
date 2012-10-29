import sys
import datetime
import csv
from google.appengine.ext import db
import google.appengine.ext.ndb as ndb
from dcf.models.transacao import Transacao
from dcf.models.transacao import Conta
from dcf.models.transacao import Dispositivo
import dcf.models.sample
import dcf.utils.remote_api as remote_api_utils
import dcf.models.sample as sample_models


remote_api_utils.configure(sys.argv[1] if len(sys.argv) > 1 else None)

contasData = csv.reader(open('csvs/contas.csv'))
contasData.next()

for conta in contasData:
    Conta(
            nome = conta[0],
            id = conta[1]
        ).put()


dispositivosData = csv.reader(open('csvs/dispositivos.csv'))

dispositivosData.next()

for dispositivo in dispositivosData:
    Dispositivo(
            id = dispositivo[0],
            idConta = dispositivo[1],
            tipo = dispositivo[2]
        ).put()

transacoesData = csv.reader(open('csvs/transacoes.csv'))
transacoesData.next()
for transacao in transacoesData:
    dataTransacao = datetime.datetime(int(transacao[7]),int(transacao[6]),int(transacao[5]),int(transacao[3]),int(transacao[4]))
    if transacao[9] == "TRUE":
        ehUmaFraude = True
    else:
        ehUmaFraude = False

    Transacao(
            idConta = transacao[0],
            idDispositivo = transacao[1],
            id = transacao[2],
            data = dataTransacao,
            valor = float(transacao[8]),
            ehFraude = ehUmaFraude,
            latitude = float(transacao[10]),
            longitude = float(transacao[11])
        ).put()
