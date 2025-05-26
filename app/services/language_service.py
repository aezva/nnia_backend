from typing import Optional
from fastapi import Request
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

class LanguageService:
    @staticmethod
    async def detect_language(
        text: str,
        preferred_language: Optional[str] = None,
        request: Optional[Request] = None
    ) -> str:
        """
        Detecta el idioma del texto o usa el idioma preferido.
        
        Args:
            text: Texto a analizar
            preferred_language: Idioma preferido del usuario
            request: Objeto Request de FastAPI para obtener headers
            
        Returns:
            Código de idioma (es, en, etc.)
        """
        # Si hay un idioma preferido, usarlo
        if preferred_language:
            return preferred_language.lower()
            
        # Si hay un request, intentar obtener el idioma del header
        if request:
            accept_language = request.headers.get("accept-language", "")
            if accept_language:
                # Tomar el primer idioma de la lista
                preferred = accept_language.split(",")[0].split(";")[0].strip()
                if preferred:
                    return preferred[:2].lower()
        
        # Si no hay preferencia, detectar el idioma
        try:
            return detect(text)
        except LangDetectException:
            return "en"  # Default a inglés si no se puede detectar

# Instancia global para usar en toda la aplicación
language_service = LanguageService() 