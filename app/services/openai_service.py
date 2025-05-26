import os
import time
import logging
from typing import Optional, Dict, Tuple
from openai import OpenAI
from dotenv import load_dotenv

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes
ASSISTANT_ID = "asst_..."  # TODO: Reemplazar con el ID real del Assistant
MAX_RETRIES = 10
RETRY_DELAY = 1  # segundos

# Inicialización del cliente
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Simulación de almacenamiento de threads (TODO: Reemplazar con persistencia real)
thread_store: Dict[str, str] = {}

async def get_or_create_thread(user_id: Optional[str], widget_id: str) -> Tuple[str, str]:
    """
    Obtiene o crea un thread para el usuario y widget dados.
    
    Args:
        user_id: ID del usuario (opcional)
        widget_id: ID del widget
        
    Returns:
        Tuple[str, str]: (thread_id, user_id)
    """
    # Generar user_id temporal si no se proporciona
    if not user_id:
        user_id = f"temp_{int(time.time())}"
    
    # Crear clave única para el par user_id-widget_id
    store_key = f"{user_id}_{widget_id}"
    
    # Si ya existe un thread, retornarlo
    if store_key in thread_store:
        return thread_store[store_key], user_id
    
    # Crear nuevo thread
    try:
        thread = client.beta.threads.create()
        thread_store[store_key] = thread.id
        return thread.id, user_id
    except Exception as e:
        logger.error(f"Error al crear thread: {str(e)}")
        raise

async def wait_for_run(thread_id: str, run_id: str) -> None:
    """
    Espera a que un run se complete.
    
    Args:
        thread_id: ID del thread
        run_id: ID del run
    """
    for _ in range(MAX_RETRIES):
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        
        if run.status == "completed":
            return
        elif run.status == "failed":
            raise Exception(f"Run falló: {run.last_error}")
        elif run.status in ["cancelled", "expired"]:
            raise Exception(f"Run {run.status}")
            
        time.sleep(RETRY_DELAY)
    
    raise Exception("Tiempo de espera agotado para el run")

async def get_last_assistant_message(thread_id: str) -> str:
    """
    Obtiene el último mensaje del assistant en el thread.
    
    Args:
        thread_id: ID del thread
        
    Returns:
        str: Contenido del último mensaje
    """
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
        order="desc",
        limit=1
    )
    
    if not messages.data:
        raise Exception("No se encontraron mensajes en el thread")
    
    message = messages.data[0]
    if message.role != "assistant":
        raise Exception("El último mensaje no es del assistant")
    
    # Obtener el contenido del mensaje
    content = message.content[0].text.value
    return content

async def ask_nnia(
    message: str,
    widget_id: str,
    user_id: Optional[str] = None,
    language: str = "es"
) -> str:
    """
    Función principal para interactuar con NNIA usando OpenAI Assistants.
    
    Args:
        message: Mensaje del usuario
        widget_id: ID del widget
        user_id: ID del usuario (opcional)
        language: Idioma de la conversación
        
    Returns:
        str: Respuesta de NNIA
    """
    try:
        # 1. Obtener o crear thread
        thread_id, user_id = await get_or_create_thread(user_id, widget_id)
        
        # 2. Enviar mensaje al thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )
        
        # 3. Lanzar run
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )
        
        # 4. Esperar a que el run termine
        await wait_for_run(thread_id, run.id)
        
        # 5. Obtener y retornar la respuesta
        response = await get_last_assistant_message(thread_id)
        return response
        
    except Exception as e:
        logger.error(f"Error en ask_nnia: {str(e)}")
        raise

# Instancia global para usar en toda la aplicación
openai_service = type('OpenAIService', (), {
    'ask_nnia': ask_nnia
})() 