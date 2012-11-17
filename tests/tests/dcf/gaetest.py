from google.appengine.ext import testbed
import unittest


class GaeTestCase(unittest.TestCase):

    def setUp(self):
        sup = super(GaeTestCase, self)
        if hasattr(sup, "setUp"):
            sup.setUp()

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

        sup = super(GaeTestCase, self)
        if hasattr(sup, "tearDown"):
            sup.tearDown()
