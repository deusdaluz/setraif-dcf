import sys

import google.appengine.ext.ndb as ndb

import dcf.utils.remote_api as remote_api_utils
import dcf.models.sample as sample_models

remote_api_utils.configure(sys.argv[1] if len(sys.argv) > 1 else None)

sample_models.Sample(
    key=ndb.Key(sample_models.Sample, "sample_id"),
    content="Bla"
).put()
