"""GasPass consts"""

import os

from dotenv import load_dotenv

load_dotenv()

CONST_API_USERNAME = os.environ.get("GASPASS_USERNAME")
CONST_API_PASSWORD = os.environ.get("GASPASS_PASSWORD")

CONST_API_BASE = "https://api.gaspass.com.br/v2"
CONST_API_LOCATOR_URL = f"{CONST_API_BASE}/get/postosproximos"
CONST_API_LOGIN_URL = f"{CONST_API_BASE}/login"
CONST_API_HEADERS = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 14; Pixel 4 XL Build/UQ1A.240205.004)",
    "Content-Type": "application/json"
}