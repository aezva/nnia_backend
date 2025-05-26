from supabase import create_client, Client
from app.core.config import get_settings

class SupabaseClient:
    _instance = None
    _client: Client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            settings = get_settings()
            cls._client = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
        return cls._instance

    @property
    def client(self) -> Client:
        return self._client

# Instancia global para usar en toda la aplicación
supabase = SupabaseClient().client 