import google.appengine.ext.ndb as ndb


class Sample(ndb.Model):
    content = ndb.StringProperty()
