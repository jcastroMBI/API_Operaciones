import os
import requests
from django.conf import settings
from rest_framework.exceptions import APIException


def obtener_token_tesoreria():
    token_url = f"{os.getenv('TESORERIA_API_BASE_URL')}/Authentication/ObtenerToken"

    login_data = {
        "usuario": os.getenv("USUARIO_TESORERIA"),
        "clave": os.getenv("CLAVE_TESORERIA"),
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('BEARER_TOKEN_TESORERIA')}",  # Si se requiere un Bearer token adicional
    }

    try:
        response = requests.post(token_url, headers=headers, json=login_data)

        response.raise_for_status()
        return response.json().get("token")
    except requests.exceptions.RequestException as e:
        raise APIException(f"Error al obtener el token de Tesorería: {str(e)}")
