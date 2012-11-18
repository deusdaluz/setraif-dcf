import google.appengine.ext.ndb as ndb
from dcf.models.transacao import Transacao

def is_fraud(transacao, conta):
    max = get_max_value(transacao, conta)
    if ((transacao.valor - max) > 1000):
    	if (transacao.valor > 1.8*max):
    		return True
    return False


def learn(transacao, conta):
    pass

def get_max_value(transacao, conta):
	key = ndb.Key('Conta', transacao.idConta)
	transacoes = Transacao.query(Transacao.idConta == transacao.idConta, Transacao.ehFraude == False).order(-Transacao.valor)
	transacao_max = transacoes.get()
	if (transacao_max is None):
		return 0
	else:
		return transacao_max.valor
