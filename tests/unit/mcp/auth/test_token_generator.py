import pytest
import time
from src.mcp.auth.token_generator import TokenGenerator
from src.mcp.auth.token_verifier import TokenVerifier

def test_token_generation_and_verification():
    secret = "test-secret"
    expiry = 3600
    generator = TokenGenerator(secret_key=secret, token_expiry=expiry)
    verifier = TokenVerifier(secret_key=secret, allowed_clients={'test-client'})

    # 1. Generate a basic token
    token = generator.generate_secure_token(client_id='test-client')
    is_valid, payload, err = verifier.verify_bearer_token(token)
    assert is_valid
    assert err is None
    assert payload['client_id'] == 'test-client'
    assert payload['exp'] > time.time()

    # 2. Generate token with IP and extra claims
    token_ip = generator.generate_secure_token(
        client_id='test-client', 
        client_ip='1.2.3.4', 
        extra_claims={'custom': 'value'}
    )
    is_valid, payload, err = verifier.verify_bearer_token(token_ip, client_ip='1.2.3.4')
    assert is_valid
    assert payload['client_ip'] == '1.2.3.4'
    assert payload['custom'] == 'value'

    # 3. Test IP mismatch
    is_valid, _, err = verifier.verify_bearer_token(token_ip, client_ip='5.6.7.8')
    assert not is_valid
    assert "IP mismatch" in err 