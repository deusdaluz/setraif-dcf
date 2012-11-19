import unittest
import datetime
from tests.dcf.gaetest import GaeTestCase
import dcf.checks.localization as localization_check
from dcf.models.transacao import Transacao
from dcf.models.transacao import Conta
from dcf.models.transacao import Dispositivo


class LocalizationCheckTestCase(GaeTestCase):


    def setUp(self):
        super(LocalizationCheckTestCase, self).setUp()
        self.sampleTransactionData = {
            "idConta": "CONTAID"
        }
        self._now = datetime.datetime.now()
        self._seq = 0



    def _new_transaction(self, lat, longi, data, is_fraud=False, idDispositivo = 'teste'):
        return Transacao(
            ehFraude=is_fraud,
            data=data,
            latitude=lat,
            longitude=longi,
            idDispositivo = idDispositivo,
            **self.sampleTransactionData
        )


    def test_localization(self):
        contaTeste = Conta(id = self.sampleTransactionData['idConta'], nome = 'Usuario1')
        contaTeste.put()
        Dispositivo(id='2001-1', idConta = self.sampleTransactionData['idConta'], tipo = 'celular').put()
        transacao1 = self._new_transaction(45.0, 0.0, self._now, False, '2001-1')
        transacao1.put()

        self.assertTrue(localization_check.is_fraud(self._new_transaction(45.0, 1.0, self._now, False, '2001-1'), contaTeste))
        self.assertFalse(localization_check.is_fraud(self._new_transaction(45.0, 1.0, self._now + datetime.timedelta(hours=1), False, '2001-1'), contaTeste))
        self.assertTrue(localization_check.is_fraud(self._new_transaction(-45.0, -90.0, self._now + datetime.timedelta(hours=1), False, '2001-1'), contaTeste))