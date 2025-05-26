from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class MessageRequest(BaseModel):
    client_id: str = Field(..., description="ID del cliente")
    role: str = Field(..., description="Rol de la conversación (ventas/soporte)")
    message: str = Field(..., description="Mensaje del usuario")

class MessageResponse(BaseModel):
    thread_id: str = Field(..., description="ID del thread de la conversación")
    response: str = Field(..., description="Respuesta de NNIA")

class TrainRequest(BaseModel):
    client_id: str = Field(..., description="ID del cliente a reentrenar")

class TrainResponse(BaseModel):
    success: bool = Field(..., description="Indica si el entrenamiento fue exitoso")
    message: str = Field(..., description="Mensaje descriptivo del resultado")

class Lead(BaseModel):
    id: str = Field(..., description="ID del lead")
    client_id: str = Field(..., description="ID del cliente")
    name: str = Field(..., description="Nombre del lead")
    email: str = Field(..., description="Email del lead")
    phone: Optional[str] = Field(None, description="Teléfono del lead")
    status: str = Field(..., description="Estado del lead")
    created_at: str = Field(..., description="Fecha de creación")

class Ticket(BaseModel):
    id: str = Field(..., description="ID del ticket")
    client_id: str = Field(..., description="ID del cliente")
    title: str = Field(..., description="Título del ticket")
    description: str = Field(..., description="Descripción del ticket")
    status: str = Field(..., description="Estado del ticket")
    priority: str = Field(..., description="Prioridad del ticket")
    created_at: str = Field(..., description="Fecha de creación")

class Message(BaseModel):
    id: str = Field(..., description="ID del mensaje")
    conversation_id: str = Field(..., description="ID de la conversación")
    role: str = Field(..., description="Rol del mensaje (user/assistant)")
    content: str = Field(..., description="Contenido del mensaje")
    created_at: str = Field(..., description="Fecha de creación")

class Conversation(BaseModel):
    id: str = Field(..., description="ID de la conversación")
    client_id: str = Field(..., description="ID del cliente")
    role: str = Field(..., description="Rol de la conversación")
    status: str = Field(..., description="Estado de la conversación")
    created_at: str = Field(..., description="Fecha de creación")
    messages: List[Message] = Field(default_factory=list, description="Mensajes de la conversación") 