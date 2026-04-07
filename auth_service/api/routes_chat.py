from fastapi import APIRouter, Depends, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase
from app.api.deps import get_chat_usecase, get_current_user_id

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase)
):
    """Отправить сообщение и получить ответ от LLM."""
    answer = await chat_usecase.ask(
        user_id=user_id,
        prompt=request.prompt,
        system=request.system,
        max_history=request.max_history,
        temperature=request.temperature
    )
    
    return ChatResponse(answer=answer)


@router.get("/history")
async def get_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase)
):
    """Получить историю сообщений пользователя."""
    history = await chat_usecase.get_history(user_id)
    return history


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase)
):
    """Очистить историю сообщений пользователя."""
    await chat_usecase.clear_history(user_id)
    return