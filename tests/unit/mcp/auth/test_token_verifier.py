import pytest
import time
import json
import base64
import hmac
import hashlib
from src.mcp.auth.token_verifier import TokenVerifier

def test_token_verification_failures():
    verifier = TokenVerifier(secret_key="test-secret", allowed_clients={'cursor-ide', 'test'})

    # 1. Invalid format
    is_valid, _, err = verifier.verify_bearer_token("invalid-token")
    assert not is_valid and "Invalid token format" in err

    # 2. Decode error
    is_valid, _, err = verifier.verify_bearer_token("mcp2.bad-base64-data")
    assert not is_valid and "Token decode error" in err

    # 3. Invalid algorithm
    bad_alg_token = base64.urlsafe_b64encode(json.dumps({"alg": "HS256"}).encode()).decode()
    is_valid, _, err = verifier.verify_bearer_token(f"mcp2.{bad_alg_token}")
    assert not is_valid and "Invalid algorithm" in err
    
    # 4. Invalid Signature
    payload = {'client_id': 'test', 'iat': 1, 'exp': 9999999999, 'jti': 'a', 'nonce': 'b'}
    token_data = {'p': payload, 's': 'bad-signature', 'alg': 'HS512'}
    bad_sig_token = base64.urlsafe_b64encode(json.dumps(token_data).encode()).decode()
    is_valid, _, err = verifier.verify_bearer_token(f"mcp2.{bad_sig_token}")
    assert not is_valid and "Invalid signature" in err

    # 5. Missing required fields
    payload = {
        'client_id': 'test',
        'exp': int(time.time()) + 3600
    }
    payload_json = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    valid_sig = hmac.new("test-secret".encode(), payload_json.encode(), hashlib.sha512).hexdigest()
    token_data = {'p': payload, 's': valid_sig, 'alg': 'HS512'}
    missing_fields_token = base64.urlsafe_b64encode(json.dumps(token_data).encode()).decode()
    is_valid, _, err = verifier.verify_bearer_token(f"mcp2.{missing_fields_token}")
    assert not is_valid and "Missing required fields" in err 

def _make_token(secret, payload):
    payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    sig = hmac.new(secret.encode(), payload_json.encode(), hashlib.sha512).hexdigest()
    token_obj = {"alg": "HS512", "p": payload, "s": sig}
    b64 = base64.urlsafe_b64encode(json.dumps(token_obj).encode()).decode().rstrip("=")
    return "mcp2." + b64

def test_verify_success():
    secret = "key"
    payload = {
        "client_id": "c1",
        "iat": int(time.time()) - 10,
        "exp": int(time.time()) + 100,
        "jti": "1",
        "nonce": "n",
    }
    tok = _make_token(secret, payload)
    ok, data, err = TokenVerifier(secret, {"c1"}).verify_bearer_token(tok)
    assert ok and err is None and data["client_id"] == "c1"

def test_verify_invalid_signature():
    secret = "key"
    payload = {"client_id": "c1", "iat": 0, "exp": 9999999999, "jti": "1", "nonce": "n"}
    bad_tok = _make_token("other", payload)  # use different secret for sig
    ok, data, err = TokenVerifier(secret, {"c1"}).verify_bearer_token(bad_tok)
    assert not ok and err == "Invalid signature" 