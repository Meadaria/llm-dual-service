import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.core.exceptions import InvalidTokenError


class TestPasswordHashing:
    def test_hash_not_equal_to_password(self):
        password = "secret123"
        hashed = hash_password(password)
        assert hashed != password

    def test_verify_correct_password(self):
        password = "secret123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        password = "secret123"
        hashed = hash_password(password)
        assert verify_password("wrong", hashed) is False


class TestJWT:
    def test_create_access_token_contains_required_fields(self):
        user_id = 1
        role = "user"
        token = create_access_token(user_id, role)
        payload = decode_token(token)
        
        assert payload is not None
        assert "sub" in payload
        assert "role" in payload
        assert "iat" in payload
        assert "exp" in payload
        assert payload["sub"] == str(user_id)
        assert payload["role"] == role

    def test_decode_token_raises_exception_for_invalid_token(self):
        invalid_token = "invalid.token.here"
        
        with pytest.raises(InvalidTokenError):
            decode_token(invalid_token)

    def test_decode_token_success_for_valid_token(self):
        user_id = 1
        role = "user"
        token = create_access_token(user_id, role)
        payload = decode_token(token)
        
        assert payload is not None
        assert payload["sub"] == str(user_id)
        assert payload["role"] == role