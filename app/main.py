import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.routes import chat, data

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración de la aplicación
settings = get_settings()
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend para el sistema NNIA - Asistente de ventas y soporte",
    debug=settings.DEBUG
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(data.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """
    Endpoint raíz que devuelve información básica de la API.
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    ) 