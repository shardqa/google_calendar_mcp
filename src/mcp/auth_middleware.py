import os
import hmac
import hashlib
import time
import base64
import json
import secrets
import ipaddress
from typing import Optional, Tuple, Dict, Set
from datetime import datetime, timedelta

class RobustAuthMiddleware:
    
    def __init__(self):
        self.secret_key = self._get_or_generate_secret()
        self.token_expiry = int(os.environ.get('MCP_TOKEN_EXPIRY', '3600'))
        self.allowed_ips = self._load_allowed_ips()
        self.allowed_clients = self._load_allowed_clients()
        self.rate_limits = {}
        self.failed_attempts = {}
        self.fixed_token = self._get_fixed_token()
        
    def _get_or_generate_secret(self) -> str:
        secret = os.environ.get('MCP_SECRET_KEY')
        if not secret:
            secret = secrets.token_urlsafe(64)
            print(f"WARNING: No MCP_SECRET_KEY found. Generated temporary key: {secret}")
            print("For production, set MCP_SECRET_KEY environment variable!")
        return secret

    def _get_fixed_token(self) -> Optional[str]:
        """Get fixed token from environment variable MCP_FIXED_TOKEN"""
        return os.environ.get('MCP_FIXED_TOKEN')
        
    def _load_allowed_ips(self) -> Set[str]:
        ips_env = os.environ.get('MCP_ALLOWED_IPS', '')
        if not ips_env:
            return set()
        return set(ip.strip() for ip in ips_env.split(','))
    
    def _load_allowed_clients(self) -> Set[str]:
        clients_env = os.environ.get('MCP_ALLOWED_CLIENTS', 'cursor-ide')
        return set(client.strip() for client in clients_env.split(','))

    def verify_fixed_token(self, token: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Verify a fixed token for permanent access"""
        if not self.fixed_token:
            return False, None, "No fixed token configured"
        
        if not hmac.compare_digest(token, self.fixed_token):
            return False, None, "Invalid fixed token"
        
        # Create a mock payload for fixed tokens
        payload = {
            'client_id': 'cursor-ide',
            'token_type': 'fixed',
            'iat': int(time.time()),
            'exp': int(time.time()) + 86400 * 365,  # 1 year
            'version': 'fixed-1.0'
        }
        
        return True, payload, None
    
    def _check_rate_limit(self, client_ip: str, max_requests: int = 100, window: int = 3600) -> bool:
        now = time.time()
        
        if client_ip not in self.rate_limits:
            self.rate_limits[client_ip] = []
        
        requests = self.rate_limits[client_ip]
        requests = [req_time for req_time in requests if now - req_time < window]
        self.rate_limits[client_ip] = requests
        
        if len(requests) >= max_requests:
            return False
            
        requests.append(now)
        return True
    
    def _record_failed_attempt(self, client_ip: str) -> None:
        now = time.time()
        if client_ip not in self.failed_attempts:
            self.failed_attempts[client_ip] = []
        
        attempts = self.failed_attempts[client_ip]
        attempts = [attempt for attempt in attempts if now - attempt < 3600]
        attempts.append(now)
        self.failed_attempts[client_ip] = attempts
    
    def _is_ip_blocked(self, client_ip: str, max_failed: int = 10) -> bool:
        if client_ip not in self.failed_attempts:
            return False
        
        now = time.time()
        recent_attempts = [
            attempt for attempt in self.failed_attempts[client_ip] 
            if now - attempt < 3600
        ]
        
        return len(recent_attempts) >= max_failed
    
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
    
    def verify_bearer_token(self, token: str, client_ip: Optional[str] = None) -> Tuple[bool, Optional[Dict], Optional[str]]:
        try:
            # First try to verify as a fixed token
            if self.fixed_token and not token.startswith('mcp2.'):
                return self.verify_fixed_token(token)
            
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
            
            # Allow tokens with allow_any_ip claim to bypass IP check
            if payload.get('allow_any_ip'):
                pass  # Skip IP verification for universal tokens
            elif client_ip and 'client_ip' in payload:
                if payload['client_ip'] != client_ip:
                    return False, None, "IP mismatch"
            
            required_fields = ['client_id', 'iat', 'exp', 'jti', 'nonce']
            if not all(field in payload for field in required_fields):
                return False, None, "Missing required fields"
                
            return True, payload, None
            
        except Exception as e:
            return False, None, f"Token verification error: {str(e)}"
    
    def check_ip_whitelist(self, client_ip: str) -> bool:
        if not self.allowed_ips:
            return True
            
        try:
            client_addr = ipaddress.ip_address(client_ip)
            for allowed_ip in self.allowed_ips:
                if '/' in allowed_ip:
                    if client_addr in ipaddress.ip_network(allowed_ip, strict=False):
                        return True
                else:
                    if str(client_addr) == allowed_ip:
                        return True
            return False
        except Exception:
            return False
    
    def authenticate_request(self, handler) -> Tuple[bool, Optional[str]]:
        client_ip = self._get_client_ip(handler)

        auth_header = handler.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            self._record_failed_attempt(client_ip)
            return False, "Missing or invalid Authorization header"

        token = auth_header[7:].strip()
        is_valid, payload, error_msg = self.verify_bearer_token(token, client_ip)

        if not is_valid:
            self._record_failed_attempt(client_ip)
            return False, error_msg or "Invalid token"

        # IP Whitelist check should happen after token verification
        # and only if the token isn't a type that bypasses IP checks (like our fixed token)
        is_fixed_token = payload.get('token_type') == 'fixed'
        allow_any_ip = payload.get('allow_any_ip', False)

        if not is_fixed_token and not allow_any_ip:
            if not self.check_ip_whitelist(client_ip):
                return False, f"IP not allowed: {client_ip}"

        if self._is_ip_blocked(client_ip):
            return False, f"IP blocked due to too many failed attempts: {client_ip}"
            
        if not self._check_rate_limit(client_ip):
            return False, f"Rate limit exceeded for IP: {client_ip}"
        
        # All checks passed
        handler.auth_payload = payload
        return True, None
    
    def _get_client_ip(self, handler) -> str:
        forwarded_for = handler.headers.get('X-Forwarded-For')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        
        real_ip = handler.headers.get('X-Real-IP')
        if real_ip:
            return real_ip.strip()
        
        return handler.client_address[0] if handler.client_address else 'unknown'
    
    def require_auth(self, handler_func):
        def wrapper(handler, *args, **kwargs):
            is_authenticated, error_msg = self.authenticate_request(handler)
            
            if not is_authenticated:
                handler.send_response(401)
                handler.send_header('Content-Type', 'application/json')
                handler.send_header('WWW-Authenticate', 'Bearer realm="MCP API"')
                handler.send_header('X-RateLimit-Remaining', '0')
                handler.end_headers()
                
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32001,
                        "message": f"Authentication failed: {error_msg}",
                        "data": {"timestamp": datetime.utcnow().isoformat()}
                    },
                    "id": None
                }
                handler.wfile.write(json.dumps(error_response).encode('utf-8'))
                return
                
            return handler_func(handler, *args, **kwargs)
        
        return wrapper
    
    def get_auth_stats(self) -> Dict:
        now = time.time()
        stats = {
            'active_rate_limits': len(self.rate_limits),
            'blocked_ips': 0,
            'recent_failed_attempts': 0,
            'fixed_token_enabled': bool(self.fixed_token)
        }
        
        for ip, attempts in self.failed_attempts.items():
            recent = [a for a in attempts if now - a < 3600]
            if len(recent) >= 10:
                stats['blocked_ips'] += 1
            stats['recent_failed_attempts'] += len(recent)
                
        return stats

auth_middleware = RobustAuthMiddleware() 