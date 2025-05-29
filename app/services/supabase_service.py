from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)

class SupabaseService:
    def __init__(self):
        settings = get_settings()
        self.client: Client = create_client(
            supabase_url=settings.SUPABASE_URL,
            supabase_key=settings.SUPABASE_KEY
        )
    
    async def get_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene información de un cliente."""
        try:
            response = self.client.table("business_details").select("*").eq("id", client_id).single().execute()
            return response.data
        except Exception as e:
            logger.error(f"Error al obtener cliente {client_id}: {str(e)}")
            return None
    
    async def get_business_info(self, client_id: str) -> List[Dict[str, Any]]:
        """Obtiene la información del negocio."""
        try:
            response = self.client.table("business_info").select("*").eq("client_id", client_id).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error al obtener business_info para {client_id}: {str(e)}")
            return []
    
    async def get_business_documents(self, client_id: str) -> List[Dict[str, Any]]:
        """Obtiene los documentos del negocio."""
        try:
            response = self.client.table("business_documents").select("*").eq("client_id", client_id).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error al obtener business_documents para {client_id}: {str(e)}")
            return []
    
    async def save_message(self, conversation_id: str, role: str, content: str) -> Optional[Dict[str, Any]]:
        """Guarda un mensaje en la conversación."""
        try:
            data = {
                "conversation_id": conversation_id,
                "role": role,
                "content": content
            }
            response = self.client.table("messages").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error al guardar mensaje: {str(e)}")
            return None
    
    async def create_conversation(self, client_id: str, role: str) -> Optional[Dict[str, Any]]:
        """Crea una nueva conversación."""
        try:
            data = {
                "client_id": client_id,
                "role": role,
                "status": "active"
            }
            response = self.client.table("conversations").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error al crear conversación: {str(e)}")
            return None
    
    async def get_conversations(self, client_id: str) -> List[Dict[str, Any]]:
        """Obtiene las conversaciones de un cliente."""
        try:
            response = self.client.table("conversations").select("*").eq("client_id", client_id).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error al obtener conversaciones para {client_id}: {str(e)}")
            return []
    
    async def get_messages(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Obtiene los mensajes de una conversación."""
        try:
            response = self.client.table("messages").select("*").eq("conversation_id", conversation_id).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error al obtener mensajes para conversación {conversation_id}: {str(e)}")
            return []
    
    async def get_leads(self, client_id: str) -> List[Dict[str, Any]]:
        """Obtiene los leads capturados."""
        try:
            response = self.client.table("captured_leads").select("*").eq("client_id", client_id).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error al obtener leads para {client_id}: {str(e)}")
            return []
    
    async def get_tickets(self, client_id: str) -> List[Dict[str, Any]]:
        """Obtiene los tickets de soporte."""
        try:
            response = self.client.table("support_tickets").select("*").eq("client_id", client_id).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error al obtener tickets para {client_id}: {str(e)}")
            return []

# Instancia global para usar en toda la aplicación
supabase_service = SupabaseService() 