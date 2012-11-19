from __future__ import absolute_import
import flask
import os

try:
    DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')
except:
    DEBUG = False

SECRET_KEY = '47e018f5adc30e4220cfa794f1339648'


def _patch_werkzeug():
    """
    A function to patch werkzeug to make it work on app engine
    """
    from werkzeug.debug.console import HTMLStringO

    def seek(self, n, mode=0):
        pass

    def readline(self):
        if len(self._buffer) == 0:
            return ''
        ret = self._buffer[0]
        del self._buffer[0]
        return ret

    # Apply all other patches.
    HTMLStringO.seek = seek
    HTMLStringO.readline = readline


def create_app():
    app = flask.Flask(__name__)
    app.debug = DEBUG
    flask.Flask.secret_key = SECRET_KEY

    import dcf.views.helloworld as helloworld_view
    app.register_blueprint(helloworld_view.bp)
    return app

app = create_app()

if DEBUG:
    import inspect
    inspect.getsourcefile = inspect.getfile

    _patch_werkzeug()

    from werkzeug import DebuggedApplication
    app = DebuggedApplication(app, evalex=True)
