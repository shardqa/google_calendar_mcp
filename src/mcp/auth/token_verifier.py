import base64
import hashlib
import hmac
import json
import time
from typing import Dict, Optional, Tuple, Set

class TokenVerifier:
    def __init__(self, secret_key: str, allowed_clients: Set[str]):
        self.secret_key = secret_key
        self.allowed_clients = allowed_clients

    def verify_bearer_token(self, token: str, client_ip: Optional[str] = None) -> Tuple[bool, Optional[Dict], Optional[str]]:
        try:
            if not token.startswith('mcp2.'):
                return False, None, "Invalid token format"
            
            token_data = token[5:]
            padding = '=' * (4 - len(token_data) % 4)
            
            try:
                decoded_bytes = base64.urlsafe_b64decode(token_data + padding)
                token_obj = json.loads(decoded_bytes.decode('utf-8'))
            except Exception:
                return False, None, "Token decode error"
            
            if token_obj.get('alg') != 'HS512':
                return False, None, "Invalid algorithm"
                
            payload = token_obj.get('p', {})
            signature = token_obj.get('s', '')
            
            payload_json = json.dumps(payload, sort_keys=True, separators=(',', ':'))
            expected_signature = hmac.new(
                self.secret_key.encode('utf-8'),
                payload_json.encode('utf-8'),
                hashlib.sha512
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                return False, None, "Invalid signature"
            
            now = int(time.time())
            if payload.get('exp', 0) < now:
                return False, None, "Token expired"
                
            if payload.get('iat', 0) > now + 300:
                return False, None, "Token from future"
            
            client_id = payload.get('client_id', '')
            if self.allowed_clients and client_id not in self.allowed_clients:
                return False, None, f"Client not allowed: {client_id}"
            
            if payload.get('allow_any_ip'):
                pass
            elif client_ip and 'client_ip' in payload:
                if payload['client_ip'] != client_ip:
                    return False, None, "IP mismatch"
            
            required_fields = ['client_id', 'iat', 'exp', 'jti', 'nonce']
            if not all(field in payload for field in required_fields):
                return False, None, "Missing required fields"
                
            return True, payload, None
            
        except Exception as e:
            return False, None, f"Token verification error: {str(e)}" 