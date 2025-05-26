import logging
from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.openai_service import openai_service

# Configuración de logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Endpoint para interactuar con NNIA.
    
    Args:
        request: Datos de la petición validados por Pydantic
        
    Returns:
        ChatResponse: Respuesta de NNIA
        
    Raises:
        HTTPException: Si ocurre un error interno
    """
    try:
        logger.info(f"Recibida petición de chat - Widget: {request.widget_id}, User: {request.user_id}")
        
        # Llamar a NNIA
        response = await openai_service.ask_nnia(
            message=request.message,
            widget_id=request.widget_id,
            user_id=request.user_id,
            language=request.language
        )
        
        logger.info(f"Respuesta generada exitosamente para Widget: {request.widget_id}")
        return ChatResponse(response=response)
        
    except Exception as e:
        logger.error(f"Error en endpoint /chat: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno al procesar la petición"
        ) 