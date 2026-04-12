from fastapi import status


class TestAuthNegative:
    def test_register_duplicate_email(self, client, test_user):
        # Первая регистрация
        client.post("/auth/register", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        
        # Вторая регистрация с тем же email
        response = client.post("/auth/register", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_login_wrong_password(self, client, test_user):
        # Регистрация
        client.post("/auth/register", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        
        # Логин с неверным паролем
        response = client.post("/auth/login", data={
            "username": test_user["email"],
            "password": "wrongpassword"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, client):
        response = client.post("/auth/login", data={
            "username": "nonexistent@example.com",
            "password": "password123"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_without_token(self, client):
        response = client.get("/auth/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_with_invalid_token(self, client):
        response = client.get("/auth/me", headers={
            "Authorization": "Bearer invalid.token.here"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED