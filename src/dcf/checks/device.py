from dcf.models.transacao import Dispositivo
import google.appengine.ext.ndb as ndb

def is_fraud(transacao, conta):
	devices = Dispositivo.query(Dispositivo.idConta == transacao.idConta)
	for device in devices.iter():
		if (transacao.idDispositivo == device.id):
			return False
	return True

def learn(transacao, conta):
    pass
