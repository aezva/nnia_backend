# NNIA Backend

Backend para el sistema NNIA construido con FastAPI, OpenAI y Supabase.

## Requisitos

- Python 3.8+
- OpenAI API Key
- Supabase URL y Key

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd backend
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

## Desarrollo

Para ejecutar el servidor de desarrollo:

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

## Documentación API

La documentación automática estará disponible en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Despliegue

Este proyecto está configurado para desplegarse en Railway. El `Procfile` ya está configurado para el despliegue.

## Estructura del Proyecto

```
backend/
├── app/
│   ├── main.py                # Punto de entrada de FastAPI
│   ├── api/                   # Endpoints organizados
│   │   └── router.py          # Ruta general de /chat, etc.
│   ├── core/
│   │   ├── config.py          # Lectura del .env
│   │   └── utils.py           # Funciones generales
│   ├── services/
│   │   ├── openai_service.py  # Comunicación con OpenAI
│   │   └── language_service.py # Detección de idioma
│   ├── models/
│   │   └── chat.py            # Esquemas de entrada/salida
│   ├── db/
│   │   └── supabase_client.py # Cliente de Supabase
└── .env.example               # Variables de entorno necesarias
``` 