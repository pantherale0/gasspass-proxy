"""GasPass API Handler."""

from datetime import datetime, timedelta

import requests
import requests.auth

from src.errors import HTTPError

from .const import (
    CONST_API_LOCATOR_URL,
    CONST_API_PASSWORD,
    CONST_API_USERNAME,
    CONST_API_LOGIN_URL,
    CONST_API_HEADERS
)

request_session = requests.sessions.Session()

_ACCESS_TOKEN = None
_REFRESH_AT = None
_LOGIN_LOCK = None

def login():
    """Login to GasPass."""
    global _ACCESS_TOKEN, _REFRESH_AT, _LOGIN_LOCK
    if _LOGIN_LOCK is None:
        _LOGIN_LOCK = True
    else:
        while _LOGIN_LOCK:
            pass
        return
    while True:
        resp = requests.get(
            CONST_API_LOGIN_URL,
            auth=requests.auth.HTTPBasicAuth(
                CONST_API_USERNAME,
                CONST_API_PASSWORD
            ),
            headers=CONST_API_HEADERS,
            timeout=30
        )
        if resp.ok:
            try:
                _ACCESS_TOKEN = resp.json()["response"]
                _REFRESH_AT = datetime.now() + timedelta(seconds=40)
            except Exception as exc:
                _LOGIN_LOCK = None
                raise exc
            _LOGIN_LOCK = None
            return
        _LOGIN_LOCK = None
        raise HTTPError(401, "invalid_auth", "The provided gaspass credentials are invalid.")

def get_fuels(lat, long, rad):
    """Get fuels from GasPass"""
    while _ACCESS_TOKEN is None or _REFRESH_AT is None or _REFRESH_AT < datetime.now():
        login()
    resp = requests.get(
        url=CONST_API_LOCATOR_URL,
        params={
            "lat": lat,
            "lng": long,
            "distance": rad,
            "max": 100,
            "dias": rad
        },
        auth=requests.auth.HTTPBasicAuth(
            username=_ACCESS_TOKEN,
            password=""
        ),
        headers=CONST_API_HEADERS,
        timeout=60
    )
    if resp.ok:
        return resp.json()
    raise HTTPError(resp.status_code, "unknown", resp.text())
