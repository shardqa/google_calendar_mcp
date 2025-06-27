import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Dict, Optional

class TokenGenerator:
    def __init__(self, secret_key: str, token_expiry: int):
        self.secret_key = secret_key
        self.token_expiry = token_expiry

    def generate_secure_token(self, client_id: str = 'cursor-ide', 
                            client_ip: Optional[str] = None,
                            extra_claims: Optional[Dict] = None) -> str:
        now = int(time.time())
        
        payload = {
            'client_id': client_id,
            'iat': now,
            'exp': now + self.token_expiry,
            'jti': secrets.token_urlsafe(32),
            'nonce': secrets.token_urlsafe(16),
            'version': '2.0'
        }
        
        if client_ip:
            payload['client_ip'] = client_ip
            
        if extra_claims:
            payload.update(extra_claims)
            
        payload_json = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            payload_json.encode('utf-8'),
            hashlib.sha512
        ).hexdigest()
        
        token_data = {
            'p': payload,
            's': signature,
            'alg': 'HS512'
        }
        
        token_json = json.dumps(token_data, separators=(',', ':'))
        encoded_token = base64.urlsafe_b64encode(token_json.encode('utf-8')).decode('ascii').rstrip('=')
        
        return f"mcp2.{encoded_token}" 