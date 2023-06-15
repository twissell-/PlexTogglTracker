from werkzeug.middleware.proxy_fix import ProxyFix
from rin import listener

listener.wsgi_app = ProxyFix(
    listener.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
listener.run(host="0.0.0.0", port=86000)
