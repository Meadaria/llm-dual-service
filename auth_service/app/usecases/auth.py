from app.repositories.users import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError


class AuthUseCase:
    """Бизнес-логика аутентификации и регистрации."""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def register(self, email: str, password: str) -> dict:
        """Регистрация нового пользователя."""
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise UserAlreadyExistsError(email)  
        
        password_hash = hash_password(password)
        user = await self.user_repo.create(email, password_hash)
        
        token = create_access_token(user.id, user.role)
        
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    
    async def login(self, email: str, password: str) -> dict:
        """Аутентификация пользователя."""
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise InvalidCredentialsError()  
        
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()  
        
        token = create_access_token(user.id, user.role)
        
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    
    async def get_profile(self, user_id: int):
        """Получение профиля пользователя по ID."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)  
        
        return user