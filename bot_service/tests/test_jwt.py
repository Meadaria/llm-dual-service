import pytest
from jose import jwt
from app.core.jwt import decode_and_validate, InvalidTokenError, TokenExpiredError
from app.core.config import settings


class TestJWT:
    def test_decode_valid_token(self):
        payload = {"sub": "123", "role": "user"}
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
        
        result = decode_and_validate(token)
        assert result["sub"] == "123"
        assert result["role"] == "user"

    def test_decode_invalid_token_raises_error(self):
        invalid_token = "invalid.token.here"
        
        with pytest.raises(InvalidTokenError):
            decode_and_validate(invalid_token)

    def test_decode_expired_token_raises_error(self):
        import time
        payload = {"sub": "123", "exp": int(time.time()) - 3600}
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
        
        with pytest.raises(TokenExpiredError):
            decode_and_validate(token)