from math import pi, cos, sin, atan2, sqrt
import google.appengine.ext.ndb as ndb
from dcf.models.transacao import Transacao
import logging
import pdb

def is_fraud(transacao, conta):
	#pdb.set_trace()
	ultima_transacao = Transacao.query(Transacao.idConta == transacao.idConta, Transacao.ehFraude == False).order(-Transacao.data).get()
	if (ultima_transacao is not None):
		#distancia em km
		distancia = lat_long_to_km(transacao.latitude, transacao.longitude, ultima_transacao.latitude, ultima_transacao.longitude)
		#tempo em horas
		tempo = abs(transacao.data - ultima_transacao.data).total_seconds() / 3600.0
		if (tempo == 0 or distancia/tempo > 800):
			return True
	return False

def learn(transacao, conta):
    pass

def lat_long_to_km(lat1, lon1, lat2, lon2):
    R = 6378.137 # Radius of earth in KM
    dLat = (lat2 - lat1) * pi / 180
    dLon = (lon2 - lon1) * pi / 180
    a = sin(dLat/2) * sin(dLat/2) + cos(lat1 * pi / 180) * cos(lat2 * pi / 180) * sin(dLon/2) * sin(dLon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = R * c
    return d