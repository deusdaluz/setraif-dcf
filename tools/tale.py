import google.appengine.ext.ndb as ndb
import json
import datetime
import time
from dcf.models.transacao import Transacao, Conta, Dispositivo
import dcf.utils.remote_api as remote_api_utils

from geventhttpclient import HTTPClient
from geventhttpclient.url import URL

import gevent


class BuyException(Exception):
    pass


class TheTaleOfACustomer(object):
    PREFIX = "tale"

    def __init__(self, hostname, id):
        self.id = id
        self.url = URL("http://{}/".format(hostname))
        self.http = HTTPClient.from_url(
            self.url, concurrency=1, network_timeout=10, connection_timeout=10
        )
        self.ntrans = 0
        self._initial_datetime = datetime.datetime.now()

    @classmethod
    def clean_db(self):
        MAX_PER_BATCH = 300
        entities = [Transacao, Conta, Dispositivo]
        for entity in entities:
            print "Deleting all tale related instances of ", entity.__name__
            cursor = ndb.Cursor()
            has_more = True
            while has_more:
                instances, cursor, has_more = entity.query(
                    entity.key >= ndb.Key(entity, self.PREFIX)
                ).fetch_page(MAX_PER_BATCH, start_cursor=cursor)
                next_batch = [
                    instance.key for instance in instances
                    if unicode(instance.id).startswith(self.PREFIX)
                ]
                if next_batch:
                    ndb.delete_multi(next_batch)
                else:
                    break
        print "Done deleting all tale related instances"

    @classmethod
    def prepare_customers(self, total, hostname):
        MAX_PER_BATCH = 200
        start = 0
        customers = []
        while start < total:
            end = min(total, start + MAX_PER_BATCH)
            print "Preparing batch of ", end-start, "customers"
            cur_batch = []
            while start < end:
                start += 1
                customer = TheTaleOfACustomer(hostname, start)
                customers.append(customer)
                cur_batch += customer.build_entities_to_put()

            ndb.put_multi(cur_batch)
            start = end

        print "Done preparing customers"
        return customers

    def build_entities_to_put(self):
        return [Conta(
            nome="The Tale Guy {}".format(self.id),
            id="{}-conta-{}".format(self.PREFIX, self.id)
        ), Dispositivo(
            id="{}-dispositivo-{}".format(self.PREFIX, self.id),
            idConta="{}-conta-{}".format(self.PREFIX, self.id),
            tipo="celular"
        )]

    def buy_something(self):
        self.ntrans += 1
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "utf-8",
            "Content-Type": "application/json; charset=utf-8",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        cur_datetime = (
            self._initial_datetime + datetime.timedelta(hours=self.ntrans)
        )

        body = json.dumps({
            "idTransaction": "{}-transacao-{}-{}".format(
                self.PREFIX, self.id, self.ntrans
            ),
            "gpsLat": "45.1244324",
            "gpsLong": "47.4234421",
            "time": cur_datetime.strftime("%H:%M:%S"),
            "date": cur_datetime.strftime("%d/%m/%Y"),
            "value": "48.70",
            "idDmtConsum": "{}-dispositivo-{}".format(self.PREFIX, self.id),
            "idAccountConsum": "{}-conta-{}".format(self.PREFIX, self.id)
        })
        resp = self.http.post("/checar", headers=headers, body=body)
        raw_data = resp.read()
        try:
            data = json.loads(raw_data)
        except:
            raise BuyException("Could not parse json: {}".format(raw_data))

        if "erroMsg" in data:
            raise BuyException("Error: {}".format(raw_data))

        if data["isFraud"] == "true":
            raise BuyException("Should not be fraud: {}".format(raw_data))

if __name__ == "__main__":
    from gevent.coros import RLock
    stats_lock = RLock()
    errors = []
    success_times = []
    error_times = []
    total_requests = 0
    REPORT_EACH = 50
    hostname = "dcf-ces63.appspot.com"
    print "Testing", hostname
    def run(customer, nreqs):
        global total_requests
        for i in range(nreqs):
            t = time.time()
            last_error = None
            try:
                customer.buy_something()
            except Exception, e:
                last_error = e
            elapsed = time.time() - t

            with stats_lock:
                if last_error is not None:
                    errors.append(last_error)
                    error_times.append(elapsed)
                else:
                    success_times.append(elapsed)
                total_requests += 1
                if total_requests % REPORT_EACH == 0:
                    print "Done", total_requests, "requests so far"

    remote_api_utils.configure(hostname)
    number_of_customers = 50
    reqs_per_customer = 2

    TheTaleOfACustomer.clean_db()
    try:
        customers = TheTaleOfACustomer.prepare_customers(number_of_customers, hostname)
        print "Waiting 5 seconds so indexes can be finished"
        time.sleep(5)
        print "Starting requests"
        initial_t = time.time()
        gevent.joinall(
            [gevent.spawn(run, c, reqs_per_customer) for c in customers]
        )
        total_elapsed = time.time() - initial_t

        # Printing stats ...
        print "Total elapsed", total_elapsed
        print "Total number of requests", total_requests
        if success_times:
            print "Avg duration", sum(success_times) / len(success_times)
        print(
            "Avg successful requests per second",
            len(success_times) / total_elapsed
        )
        print(
            "Number of detected frauds",
            sum(1 for e in errors if "Should not be fraud" in unicode(e))
        )
        print "Number of errors", len(errors)

    finally:
        TheTaleOfACustomer.clean_db()

    if errors:
        fname = raw_input("Filename to store errors or empty to abort: ")
        if fname:
            with open(fname, "w+") as f:
                f.write("\n".join(unicode(e) for e in errors))
