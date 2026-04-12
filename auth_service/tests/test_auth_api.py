from fastapi import status


class TestAuthAPI:
    def test_register_success(self, client, test_user):
        response = client.post("/auth/register", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_success(self, client, test_user):
        # Сначала регистрируем
        client.post("/auth/register", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        
        # Затем логинимся
        response = client.post("/auth/login", data={
            "username": test_user["email"],
            "password": test_user["password"]
        })
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()

    def test_me_with_valid_token(self, client, test_user):
        # Регистрация
        register_response = client.post("/auth/register", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        
        # Если пользователь уже существует, логинимся
        if register_response.status_code == 409:
            login_response = client.post("/auth/login", data={
                "username": test_user["email"],
                "password": test_user["password"]
            })
            token = login_response.json()["access_token"]
        else:
            token = register_response.json()["access_token"]
        
        # Запрос профиля
        response = client.get("/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == test_user["email"]