from tests.dcf.gaetest import GaeTestCase
from dcf.models.transacao import *
import dcf
import json

import dcf.views.helloworld as helloworld



class PresentationTaleTestCase(GaeTestCase):

    def setUp(self):
        super(PresentationTaleTestCase, self).setUp()
        Conta(
            id="conta",
            nome="Meu nome"
        ).put()
        Dispositivo(
            id="dispositivo",
            idConta="conta",
            tipo="celular"
        ).put()
        self.test_client = dcf.create_app().test_client()

    def submit_transaction(self, data):
        response = self.test_client.post(
            "/checar", data=json.dumps(data),
            content_type='application/json')
        self.assertEquals(response.status_code, 200, msg=response.data)
        resp_data = json.loads(response.data)
        self.assertFalse("erroMsg" in resp_data, msg=response.data)
        self.assertTrue("isFraud" in resp_data, msg=response.data)
        self.assertTrue(
            resp_data["isFraud"] in ["true", "false"],
            msg=response.data
        )
        return resp_data["isFraud"] == "true"

    def test_presentation_tale(self):
        self.assertFalse(
            self.submit_transaction({
              "idTransaction":"1",
              "gpsLat":"-23.2107",
              "gpsLong":"-45.877",
              "time":"14:23:01",
              "date":"18/11/2012",
              "value":"23.70",
              "idDmtConsum":"dispositivo",
              "idAccountConsum":"conta"
            })
        )
        self.assertFalse(
            self.submit_transaction({
              "idTransaction":"2",
              "gpsLat":"-23.2045",
              "gpsLong":"-45.8715",
              "time":"14:43:01",
              "date":"18/11/2012",
              "value":"245.70",
              "idDmtConsum":"dispositivo",
              "idAccountConsum":"conta"
            })
        )
        self.assertFalse(
            self.submit_transaction({
              "idTransaction":"3",
              "gpsLat":"-23.2008",
              "gpsLong":"-45.8810",
              "time":"20:05:31",
              "date":"18/11/2012",
              "value":"375.60",
              "idDmtConsum":"dispositivo",
              "idAccountConsum":"conta"
            })
        )
        self.assertTrue(
            self.submit_transaction({
              "idTransaction":"4",
              "gpsLat":"-23.2008",
              "gpsLong":"-45.8810",
              "time":"20:23:01",
              "date":"18/11/2012",
              "value":"4830.63",
              "idDmtConsum":"dispositivo",
              "idAccountConsum":"conta"
            })
        )
        self.assertFalse(
            self.submit_transaction({
              "idTransaction":"5",
              "gpsLat":"-23.4808",
              "gpsLong":"-46.5410",
              "time":"08:23:01",
              "date":"19/11/2012",
              "value":"228.00",
              "idDmtConsum":"dispositivo",
              "idAccountConsum":"conta"
            })
        )
        self.assertFalse(
            self.submit_transaction({
              "idTransaction":"6",
              "gpsLat":"-3.7308",
              "gpsLong":"-38.5410",
              "time":"15:01:00",
              "date":"19/11/2012",
              "value":"454.02",
              "idDmtConsum":"dispositivo",
              "idAccountConsum":"conta"
            })
        )
        self.assertTrue(
            self.submit_transaction({
              "idTransaction":"7",
              "gpsLat":"28.5308",
              "gpsLong":"-81.3710",
              "time":"16:23:01",
              "date":"19/11/2012",
              "value":"208.54",
              "idDmtConsum":"dispositivo",
              "idAccountConsum":"conta"
            })
        )
        self.assertTrue(
            self.submit_transaction({
              "idTransaction":"8",
              "gpsLat":"-23.2045",
              "gpsLong":"-45.8715",
              "time":"03:23:01",
              "date":"20/11/2012",
              "value":"408.40",
              "idDmtConsum":"DMX123V",
              "idAccountConsum":"conta"
            })
        )