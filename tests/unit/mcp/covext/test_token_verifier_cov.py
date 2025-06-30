import json, time, hmac, base64, hashlib
from src.mcp.auth.token_verifier import TokenVerifier


def _make(secret, **ov):
    p = {
        "client_id": "c",
        "iat": int(time.time()) - 1,
        "exp": int(time.time()) + 30,
        "jti": "j",
        "nonce": "n",
    }
    p.update(ov)
    pj = json.dumps(p, sort_keys=True, separators=(",", ":"))
    sig = hmac.new(secret.encode(), pj.encode(), hashlib.sha512).hexdigest()
    obj = {"alg": "HS512", "p": p, "s": sig}
    enc = base64.urlsafe_b64encode(json.dumps(obj).encode()).decode().rstrip("=")
    return f"mcp2.{enc}"


def test_token_paths():
    sk = "s"
    good = _make(sk)
    tv = TokenVerifier(sk, {"c"})
    assert tv.verify_bearer_token(good)[0]
    bad = good[:-1] + ("A" if good[-1] != "A" else "B")
    assert not tv.verify_bearer_token(bad)[0]
    exp = _make(sk, exp=int(time.time()) - 5)
    assert not tv.verify_bearer_token(exp)[0]
    tv2 = TokenVerifier(sk, {"x"})
    assert not tv2.verify_bearer_token(good)[0] 