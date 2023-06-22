from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from rin import plex_listener

rin = Flask("rin")

rin.register_blueprint(plex_listener)

rin.wsgi_app = ProxyFix(rin.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
rin.run(host="0.0.0.0", port=86000)
