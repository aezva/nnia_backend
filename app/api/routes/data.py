import logging
from typing import List
from fastapi import APIRouter, HTTPException
from app.models.api import Lead, Ticket, Conversation
from app.services.supabase_service import supabase_service

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/leads/{client_id}", response_model=List[Lead])
async def get_leads(client_id: str) -> List[Lead]:
    """
    Obtiene los leads capturados para un cliente.
    """
    try:
        # Verificar que el cliente existe
        client = await supabase_service.get_client(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Obtener leads
        leads = await supabase_service.get_leads(client_id)
        return [Lead(**lead) for lead in leads]
        
    except Exception as e:
        logger.error(f"Error en endpoint /leads: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno al obtener leads"
        )

@router.get("/tickets/{client_id}", response_model=List[Ticket])
async def get_tickets(client_id: str) -> List[Ticket]:
    """
    Obtiene los tickets de soporte para un cliente.
    """
    try:
        # Verificar que el cliente existe
        client = await supabase_service.get_client(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Obtener tickets
        tickets = await supabase_service.get_tickets(client_id)
        return [Ticket(**ticket) for ticket in tickets]
        
    except Exception as e:
        logger.error(f"Error en endpoint /tickets: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno al obtener tickets"
        )

@router.get("/conversations/{client_id}", response_model=List[Conversation])
async def get_conversations(client_id: str) -> List[Conversation]:
    """
    Obtiene las conversaciones y mensajes para un cliente.
    """
    try:
        # Verificar que el cliente existe
        client = await supabase_service.get_client(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Obtener conversaciones
        conversations = await supabase_service.get_conversations(client_id)
        
        # Obtener mensajes para cada conversación
        result = []
        for conv in conversations:
            messages = await supabase_service.get_messages(conv["id"])
            conversation = Conversation(
                **conv,
                messages=[Message(**msg) for msg in messages]
            )
            result.append(conversation)
        
        return result
        
    except Exception as e:
        logger.error(f"Error en endpoint /conversations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno al obtener conversaciones"
        ) 