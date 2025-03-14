# -------------------------------
# Etapa base: Construcción y preparación
# -------------------------------
FROM python:3.11.6-slim AS base

# Instalar dependencias del sistema comunes (si es necesario para ambos)
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc \
    unixodbc-dev \
    odbcinst \
    libodbc1 \
    && apt-get clean

WORKDIR /app

# Copiar únicamente los archivos necesarios para instalar dependencias
COPY requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente
COPY . .

# -------------------------------
# Target para la API (producción de la API)
# -------------------------------
FROM base AS api

# Instalar dependencias específicas del sistema para la API (msodbcsql17)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean

# Crear las carpetas donde se guardarán los archivos estáticos para la API
RUN mkdir -p /home/app/web/staticfiles

# Exponer el puerto en tiempo de construcción
EXPOSE 8000

# Comando para correr la API con Gunicorn en el puerto definido
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8000 API_Operaciones.wsgi:application"]

# -------------------------------
# Target para la Documentación (Docs)
# -------------------------------
FROM base AS docs

# Exponer el puerto en tiempo de construcción
EXPOSE 8001

# Comando para correr la instancia de Docs usando un settings especial
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8001 API_Operaciones.wsgi:application --env DJANGO_SETTINGS_MODULE=API_Operaciones.settings_docs"]
