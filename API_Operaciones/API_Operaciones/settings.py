from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY")  # SECURITY WARNING
PASSWORD_STATIC_SALT = os.getenv("SALT")
DEBUG = False  # SECURITY WARNING
ALLOWED_HOSTS = ["*"]

# Configuracion de HTTPS
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Aplicaciones instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Aplicaciones internas
    "authentification",
    "operaciones",
    "logs_operaciones",
    # Librerías externas
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "logs_operaciones.middleware.APILoggingMiddleware",
    "authentification.middleware.RestrictOriginMiddleware",
]

# Configuración de URLs y WSGI
ROOT_URLCONF = "API_Operaciones.urls"
WSGI_APPLICATION = "API_Operaciones.wsgi.application"

# Configuración de autenticación y DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Configuración de JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# Configuración de bases de datos externas (SQL Server)
DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": os.getenv("SQL_SERVER_DB_NAME_APLICACION"),
        "USER": os.getenv("SQL_SERVER_USER"),
        "PASSWORD": os.getenv("SQL_SERVER_PASSWORD"),
        "HOST": os.getenv("SQL_SERVER_HOST_APLICACION"),
        "PORT": os.getenv("SQL_SERVER_PORT_APLICACION"),
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server"},
    },
    "bcsmbi_online": {
        "ENGINE": "mssql",
        "NAME": os.getenv("SQL_SERVER_DB_NAME_REPLICA"),
        "USER": os.getenv("SQL_SERVER_USER"),
        "PASSWORD": os.getenv("SQL_SERVER_PASSWORD"),
        "HOST": os.getenv("SQL_SERVER_HOST_REPLICA"),
        "PORT": os.getenv("SQL_SERVER_PORT_REPLICA"),
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server"},
    },
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internacionalización y zona horaria
LANGUAGE_CODE = "es-es"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# Configuración de archivos estáticos y medios
STATIC_URL = "/static/"
STATIC_ROOT = "/home/app/web/staticfiles"

# Configuración de CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    url for url in [os.getenv("FRONTEND_URL"), os.getenv("DOCS_URL")] if url
] + os.getenv("CORS_EXTRA_ORIGINS", "").splitlines()
CSRF_TRUSTED_ORIGINS = [os.getenv("SELF_URL")]

# Configuración de templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Configuración de documentación con Spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "MBI - Agentes API",
    "DESCRIPTION": (
        "Documentación para API Agentes MBI.\n\n"
        "**Nota:** Todos los endpoints mostrados en esta documentación están bloqueados "
        "por restricciones de origen. Solo se pueden acceder desde orígenes autorizados."
    ),
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "SERVE_INCLUDE_SCHEMA": False,
    "PREPROCESSING_HOOKS": ["authentification.hooks.swagger_preprocessing_hook"],
}

# Configuración de modelo de usuario personalizado
AUTH_USER_MODEL = "authentification.AgenteUser"

PASSWORD_HASHERS = [
    "authentification.hashers.PBKDF2PasswordHasher",
]

# Configuración de caché en memoria
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Configuración de logging de API
DRF_API_LOGGER_DATABASE = True

# Configuración específica de la API de Optimus
OPTIMUS_API_BASE_URL = "http://mbiservicios.optimuscb.cl:9055"

# Configuración del campo de clave primaria por defecto
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
