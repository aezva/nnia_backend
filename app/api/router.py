from fastapi import APIRouter, Request
from app.models.chat import ChatRequest, ChatResponse
from app.services.openai_service import openai_service
from app.services.language_service import language_service
from app.api.chat import router as chat_router

router = APIRouter()

# Incluir el router de chat
router.include_router(chat_router, prefix="/api/v1")

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    """
    Endpoint principal para el chat con IA.
    """
    # Detectar el idioma
    language = await language_service.detect_language(
        text=request.messages[-1].content,
        preferred_language=request.preferred_language,
        request=req
    )
    
    # Obtener respuesta de OpenAI
    response = await openai_service.send_message(
        messages=[msg.dict() for msg in request.messages],
        model=request.model,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    
    # Añadir el idioma detectado a la respuesta
    response["language"] = language
    
    return ChatResponse(**response) 