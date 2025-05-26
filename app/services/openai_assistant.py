import os
import time
import logging
from typing import Optional, Dict, Any, List
from openai import OpenAI
from app.core.config import get_settings
from app.services.supabase_service import supabase_service

logger = logging.getLogger(__name__)

class OpenAIAssistantService:
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.assistant_store: Dict[str, str] = {}  # client_id -> assistant_id
    
    async def get_or_create_assistant(self, client_id: str) -> str:
        """
        Obtiene o crea un assistant para el cliente.
        """
        if client_id in self.assistant_store:
            return self.assistant_store[client_id]
        
        # Obtener información del cliente
        client = await supabase_service.get_client(client_id)
        if not client:
            raise Exception(f"Cliente {client_id} no encontrado")
        
        # Obtener información del negocio
        business_info = await supabase_service.get_business_info(client_id)
        business_docs = await supabase_service.get_business_documents(client_id)
        
        # Crear el assistant
        try:
            assistant = self.client.beta.assistants.create(
                name=f"NNIA Assistant - {client.get('name', 'Cliente')}",
                instructions=self._create_instructions(client, business_info, business_docs),
                model="gpt-4-turbo-preview",
                tools=[{"type": "retrieval"}]
            )
            
            self.assistant_store[client_id] = assistant.id
            return assistant.id
            
        except Exception as e:
            logger.error(f"Error al crear assistant para {client_id}: {str(e)}")
            raise
    
    def _create_instructions(
        self,
        client: Dict[str, Any],
        business_info: List[Dict[str, Any]],
        business_docs: List[Dict[str, Any]]
    ) -> str:
        """
        Crea las instrucciones para el assistant basadas en la información del cliente.
        """
        instructions = [
            "Eres NNIA, un asistente de ventas y soporte para negocios.",
            f"Estás ayudando a {client.get('name', 'el cliente')}.",
            f"Idioma preferido: {client.get('lang', 'es')}",
            "\nInformación del negocio:"
        ]
        
        # Agregar información del negocio
        for info in business_info:
            instructions.append(f"- {info.get('title', '')}: {info.get('content', '')}")
        
        # Agregar documentos
        if business_docs:
            instructions.append("\nDocumentos disponibles:")
            for doc in business_docs:
                instructions.append(f"- {doc.get('title', '')}: {doc.get('summary', '')}")
        
        return "\n".join(instructions)
    
    async def train_assistant(self, client_id: str) -> bool:
        """
        Reentrena el assistant con la información actualizada del cliente.
        """
        try:
            # Eliminar assistant existente si hay uno
            if client_id in self.assistant_store:
                await self.client.beta.assistants.delete(self.assistant_store[client_id])
                del self.assistant_store[client_id]
            
            # Crear nuevo assistant
            await self.get_or_create_assistant(client_id)
            return True
            
        except Exception as e:
            logger.error(f"Error al reentrenar assistant para {client_id}: {str(e)}")
            return False
    
    async def send_message(
        self,
        client_id: str,
        message: str,
        thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envía un mensaje al assistant y obtiene la respuesta.
        """
        try:
            # Obtener o crear assistant
            assistant_id = await self.get_or_create_assistant(client_id)
            
            # Crear o usar thread existente
            if not thread_id:
                thread = self.client.beta.threads.create()
                thread_id = thread.id
            
            # Enviar mensaje
            self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message
            )
            
            # Ejecutar assistant
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            
            # Esperar respuesta
            while True:
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
                
                if run_status.status == "completed":
                    break
                elif run_status.status in ["failed", "cancelled", "expired"]:
                    raise Exception(f"Run {run_status.status}")
                
                time.sleep(1)
            
            # Obtener respuesta
            messages = self.client.beta.threads.messages.list(
                thread_id=thread_id,
                order="desc",
                limit=1
            )
            
            if not messages.data:
                raise Exception("No se encontró respuesta")
            
            response = messages.data[0]
            return {
                "thread_id": thread_id,
                "response": response.content[0].text.value
            }
            
        except Exception as e:
            logger.error(f"Error al enviar mensaje: {str(e)}")
            raise

# Instancia global para usar en toda la aplicación
openai_assistant = OpenAIAssistantService() 