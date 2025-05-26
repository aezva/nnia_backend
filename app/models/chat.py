from pydantic import BaseModel, Field
from typing import List, Optional

class Message(BaseModel):
    role: str = Field(..., description="Rol del mensaje (user, assistant, system)")
    content: str = Field(..., description="Contenido del mensaje")

class ChatRequest(BaseModel):
    message: str = Field(..., description="Mensaje del usuario")
    widget_id: str = Field(..., description="ID del widget")
    user_id: Optional[str] = Field(None, description="ID del usuario (opcional)")
    language: Optional[str] = Field("es", description="Idioma preferido del usuario")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Respuesta de NNIA")
    role: str = Field(..., description="Rol de la respuesta")
    finish_reason: str = Field(..., description="Razón de finalización")
    language: str = Field(..., description="Idioma detectado") 