from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase
from app.api.deps import get_auth_usecase, get_current_user_id

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(
    request: RegisterRequest,
    auth_usecase: AuthUseCase = Depends(get_auth_usecase)
):
    """Регистрация нового пользователя."""
    result = await auth_usecase.register(request.email, request.password)
    return result


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase)
):
    """Аутентификация пользователя (OAuth2)."""
    result = await auth_usecase.login(form_data.username, form_data.password)
    return result


@router.get("/me", response_model=UserPublic)
async def get_profile(
    user_id: int = Depends(get_current_user_id),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase)
):
    """Получение профиля текущего пользователя."""
    user = await auth_usecase.get_profile(user_id)
    return user