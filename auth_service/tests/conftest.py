import os
import pytest
from fastapi.testclient import TestClient

# Удаляем старую БД перед каждым запуском тестов
DB_PATH = "./test.db"
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

os.environ["SQLITE_PATH"] = DB_PATH

from app.main import app


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    # После всех тестов удаляем БД
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_user():
    return {
        "email": "student_ivanov@email.com",
        "password": "password123"
    }