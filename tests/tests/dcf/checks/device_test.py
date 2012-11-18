import unittest
import datetime
from tests.dcf.gaetest import GaeTestCase
import dcf.checks.device as device_check
from dcf.models.transacao import Transacao
from dcf.models.transacao import Conta
from dcf.models.transacao import Dispositivo


class DeviceCheckTestCase(GaeTestCase):


    def setUp(self):
        super(DeviceCheckTestCase, self).setUp()
        self.sampleTransactionData = {
            "idConta": "CONTAID"
        }
        self._now = datetime.datetime.now()
        self._seq = 0



    def _new_transaction(self, value, is_fraud=False, idDispositivo = 'teste'):
        self._seq += 1
        return Transacao(
            valor=value,
            ehFraude=is_fraud,
            data=self._now + datetime.timedelta(hours=self._seq),
            idDispositivo = idDispositivo,
            **self.sampleTransactionData
        )


    def test_device(self):
        contaTeste = Conta(id = self.sampleTransactionData['idConta'], nome = 'Usuario1')
        contaTeste.put()
        Dispositivo(id='2001-1', idConta = self.sampleTransactionData['idConta'], tipo = 'celular').put()
        Dispositivo(id='2001-2', idConta = self.sampleTransactionData['idConta'], tipo = 'computador').put()

        self.assertFalse(device_check.is_fraud(self._new_transaction(100.0, False, '2001-1'), contaTeste))
        self.assertFalse(device_check.is_fraud(self._new_transaction(100.0, False, '2001-2'), contaTeste))
        self.assertTrue(device_check.is_fraud(self._new_transaction(100.0, False, 'QUALQUERCOISA'), contaTeste))