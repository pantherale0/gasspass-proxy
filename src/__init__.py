from flask import jsonify
from flask_openapi3 import Info, OpenAPI
from werkzeug.exceptions import HTTPException

from ._version import VERSION
from .limiter import limiter
from .blueprints import ProxyServiceApi
from .errors import HTTPError, NotFound

info = Info(
    title="GasPass Proxy",
    version=VERSION
)
app = OpenAPI(__name__, info=info)

# register routes
app.register_api(ProxyServiceApi)

@app.errorhandler(HTTPError)
def handle_app_error(exc: HTTPError):
    """Handle an error from the app."""
    response = jsonify(exc.details)
    response.status_code = exc.response
    return response

@app.errorhandler(Exception)
def handle_global_exc(exc):
    """Handle a globally raised exception."""
    details = {
        "code": "unknown",
        "message": str(exc)
    }
    if isinstance(exc, HTTPException):
        if exc.code == 404:
            return handle_app_error(NotFound())
        details["code"] = str(exc.code)
        status_code = exc.code
    else:
        status_code = 500
    response = jsonify(details)
    response.status_code = status_code
    return response

limiter.init_app(app)
print(f"Limiter state: {limiter.enabled}")

if __name__ == '__main__':
    print("Starting applet")
    app.run()
