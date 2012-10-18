import google.appengine.ext.ndb as ndb


class Transacao(ndb.Model):
    idConta = ndb.StringProperty(indexed=True)
    idDispositivo = ndb.StringProperty(indexed=True)
    idTransacao = ndb.StringProperty(indexed=True)
    data = ndb.DateProperty(indexed = True)
    valor = ndb.FloatProperty(indexed = True)
    ehFraude = ndb.BooleanProperty(indexed = True)
    latitude = ndb.FloatProperty(indexed = True)
    longitude = ndb.FloatProperty(indexed = True)

class Dispositivo(ndb.Model):
    idConta = ndb.StringProperty(indexed=True)
    idDispositivo = ndb.StringProperty(indexed=True)
    tipo = ndb.StringProperty(indexed=True)
    

class Conta(ndb.Model):
    idConta = ndb.StringProperty(indexed=True)
    nome = ndb.StringProperty(indexed=True)


class Pessoa(ndb.Model):
    nome = ndb.StringProperty(indexed=True)
    idade = ndb.IntegerProperty(indexed=True)
