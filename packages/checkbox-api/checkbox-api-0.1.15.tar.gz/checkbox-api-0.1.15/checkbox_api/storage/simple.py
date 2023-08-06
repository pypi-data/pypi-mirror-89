from dataclasses import dataclass
from typing import Any, Dict, Optional

import jwt


@dataclass
class SessionStorage:
    def __init__(self, token: Optional[str] = None, license_key: Optional[str] = None):
        self.token = token
        self.license_key = license_key
        self.cashier = None
        self.cash_register = None
        self.shift = None

    @property
    def headers(self):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if self.license_key:
            headers["X-License-Key"] = self.license_key
        return headers

    @property
    def token_data(self) -> Optional[Dict[str, Any]]:
        if self.token:
            return jwt.decode(self.token, verify=False)
        return None
