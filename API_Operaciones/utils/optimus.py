import os
import requests
from django.conf import settings
from rest_framework.exceptions import APIException

def obtener_token_optimus():
    token_url = f"{settings.OPTIMUS_API_BASE_URL}/api/Session/obtenerToken"

    login_data = {
        "IdEmpresa": int(os.getenv('ID_EMPRESA_OPTIMUS')),
        "IdCodigo": os.getenv('CODIGO_OPTIMUS'),
        "Password": os.getenv('PASSWORD_OPTIMUS'),
        "IdCanal": "",
    }

    headers = {
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(token_url, headers=headers, json=login_data)
        response.raise_for_status()
        return response.json().get('Token')
    except requests.exceptions.RequestException as e:
        raise APIException(f"Error al obtener el token de Optimus: {str(e)}")
