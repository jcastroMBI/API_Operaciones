from .settings import *

ROOT_URLCONF = "API_Operaciones.urls_docs"

# Permitir cualquier origen en el entorno de documentación
CORS_ALLOW_ALL_ORIGINS = True  # Permite cualquier origen
CORS_ALLOWED_ORIGINS = []  # Se desactiva la lista específica
CSRF_TRUSTED_ORIGINS = []  # Evita problemas con CSRF si no es necesario
CORS_ALLOW_CREDENTIALS = False  # Deshabilita credenciales para mayor seguridad
