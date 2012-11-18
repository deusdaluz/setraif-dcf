import unittest
import datetime
from tests.dcf.gaetest import GaeTestCase
import dcf.checks.value as value_check
from dcf.models.transacao import Transacao


class ValueCheckTestCase(GaeTestCase):

    def setUp(self):
        super(ValueCheckTestCase, self).setUp()
        self.sampleTransactionData = {
            "idConta": "CONTAID"
        }
        self._now = datetime.datetime.now()
        self._seq = 0

    def _new_transaction(self, value, is_fraud=False):
        self._seq += 1
        return Transacao(
            valor=value,
            ehFraude=is_fraud,
            data=self._now + datetime.timedelta(hours=self._seq),
            **self.sampleTransactionData
        )

    def test_small_value_and_no_prev_transactions(self):
        self.assertFalse(
            value_check.is_fraud(self._new_transaction(100.00), None)
        )

    def test_small_value_and_a_prev_small_transaction(self):
        self._new_transaction(100.00).put()
        self.assertFalse(
            value_check.is_fraud(self._new_transaction(100.00), None)
        )

    def test_big_value_and_no_prev_transactions(self):
        self.assertTrue(
            value_check.is_fraud(self._new_transaction(1001.00), None)
        )

    def test_big_value_and_a_prev_fraud_transaction(self):
        self._new_transaction(100.00, is_fraud=True).put()
        self.assertTrue(
            value_check.is_fraud(self._new_transaction(1001.00), None)
        )

    def test_big_value_and_a_prev_small_transaction(self):
        self._new_transaction(100.00).put()
        self.assertTrue(
            value_check.is_fraud(self._new_transaction(1101.00), None)
        )

    def test_big_value_and_a_prev_big_transaction(self):
        self._new_transaction(600.00).put()
        self.assertFalse(
            value_check.is_fraud(self._new_transaction(1001.00), None)
        )
