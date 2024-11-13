"""Rate limiter."""

from datetime import datetime, timezone

from flask import request, jsonify
from flask_limiter import Limiter, RequestLimit
from flask_limiter.util import get_remote_address

def rate_limit_breach(limit: RequestLimit):
    """Rate limiter."""
    details = {
        "code": "rate_limit",
        "details": "Rate limit exceeded, try again later."
    }
    response = jsonify(details)
    response.status_code = 429
    response.headers.add_header(
        "Retry-After",
        limit.reset_at-datetime.now().replace(tzinfo=timezone.utc).timestamp()
    )
    return response

limiter = Limiter(
    storage_uri="memory://",
    on_breach=rate_limit_breach,
    key_func=get_remote_address
)

@limiter.request_filter
def ip_whitelist():
    return request.remote_addr == "127.0.0.1"
