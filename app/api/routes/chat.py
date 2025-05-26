import logging
from fastapi import APIRouter, HTTPException
from app.models.api import (
    MessageRequest,
    MessageResponse,
    TrainRequest,
    TrainResponse
)
from app.services.openai_assistant import openai_assistant
from app.services.supabase_service import supabase_service

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/message", response_model=MessageResponse)
async def send_message(request: MessageRequest) -> MessageResponse:
    """
    Envía un mensaje a NNIA y obtiene la respuesta.
    """
    try:
        # Verificar que el cliente existe
        client = await supabase_service.get_client(request.client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Obtener o crear conversación
        conversations = await supabase_service.get_conversations(request.client_id)
        conversation = next(
            (c for c in conversations if c["role"] == request.role and c["status"] == "active"),
            None
        )
        
        if not conversation:
            conversation = await supabase_service.create_conversation(
                request.client_id,
                request.role
            )
            if not conversation:
                raise HTTPException(status_code=500, detail="Error al crear conversación")
        
        # Guardar mensaje del usuario
        user_message = await supabase_service.save_message(
            conversation["id"],
            "user",
            request.message
        )
        if not user_message:
            raise HTTPException(status_code=500, detail="Error al guardar mensaje")
        
        # Obtener respuesta de NNIA
        response = await openai_assistant.send_message(
            request.client_id,
            request.message,
            conversation.get("thread_id")
        )
        
        # Guardar respuesta de NNIA
        assistant_message = await supabase_service.save_message(
            conversation["id"],
            "assistant",
            response["response"]
        )
        if not assistant_message:
            raise HTTPException(status_code=500, detail="Error al guardar respuesta")
        
        return MessageResponse(
            thread_id=response["thread_id"],
            response=response["response"]
        )
        
    except Exception as e:
        logger.error(f"Error en endpoint /message: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno al procesar el mensaje"
        )

@router.post("/train", response_model=TrainResponse)
async def train_assistant(request: TrainRequest) -> TrainResponse:
    """
    Reentrena el assistant con la información actualizada del cliente.
    """
    try:
        # Verificar que el cliente existe
        client = await supabase_service.get_client(request.client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Reentrenar assistant
        success = await openai_assistant.train_assistant(request.client_id)
        
        if success:
            return TrainResponse(
                success=True,
                message="Assistant reentrenado exitosamente"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Error al reentrenar el assistant"
            )
            
    except Exception as e:
        logger.error(f"Error en endpoint /train: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno al reentrenar el assistant"
        ) 