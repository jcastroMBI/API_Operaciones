from django.conf import settings
from django.db import connections

from datetime import datetime

import requests

from rest_framework.exceptions import (
    ValidationError,
    APIException,
)


def cliente_pertenece_agente(codigoAgente, documento_identidad):
    with connections["bcsmbi_online"].cursor() as cursor:
        validacion_query = """
            SELECT 
                cliper.DocumentoIdentidad AS documento_identidad_clipersona
            FROM 
                [BCSMBI_ONLINE].[dbo].[SocioNegocio_Cliente] AS cli
            LEFT JOIN 
                [BCSMBI_ONLINE].[dbo].[SocioNegocio_Persona] AS age 
                ON cli.IdPersonaEjecutivo = age.IdPersona
            LEFT JOIN 
                [BCSMBI_ONLINE].[dbo].[SocioNegocio_Persona] AS cliper 
                ON cliper.IdDocumentoIdentidad = cli.IdDocumentoIdentidad
            WHERE 
                cli.IdPersonaEjecutivo = %s
        """
        cursor.execute(validacion_query, codigoAgente)
        clientes_usuario = [row[0] for row in cursor.fetchall()]

    if documento_identidad not in clientes_usuario:
        return False

    return True


def custodia_suficiente(
    optimusToken, documento_identidad, codigo_portafolio, nemotecnico, cantidad
):
    custodia_url = f"{settings.OPTIMUS_API_BASE_URL}/api/Custodia/consultarCustodia"
    custodia_headers = {
        "accept": "application/json",
        "X-SESSION-TOKEN": optimusToken,
        "Content-Type": "application/json",
    }

    custodia_data = {
        "IdEmpresa": 0,
        "IdUsuario": "string",
        "ClaveUsuario": "string",
        "Custodia": [
            {
                "IdInterno": 0,
                "FechaConsulta": datetime.now().strftime("%Y-%m-%d"),
                "Filtro": "DocumentoIdentidad",
                "Valor": documento_identidad,
            },
            {
                "IdInterno": 0,
                "FechaConsulta": "",
                "Filtro": "CodigoPortafolio",
                "Valor": codigo_portafolio,
            },
        ],
    }

    try:
        api_response = requests.post(
            custodia_url, headers=custodia_headers, json=custodia_data
        )
        api_response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise APIException(e)

    custodia_result = api_response.json().get("Custodia", [])

    custodia_dict = {
        custodia["IdEmisor"]: custodia["CantidadCustodia"]
        for custodia in custodia_result
    }

    if nemotecnico not in custodia_dict:
        raise ValidationError(
            f"No se encontró custodia para el instrumento {nemotecnico}."
        )

    cantidad_custodia = custodia_dict[nemotecnico]

    if cantidad_custodia < cantidad:
        raise ValidationError(
            f"Cantidad insuficiente en custodia. "
            f"Cantidad disponible: {round(cantidad_custodia)}, "
            f"Cantidad requerida: {cantidad}"
        )


def saldo_suficiente(
    optimusToken, documento_identidad, codigo_portafolio, monto, moneda
):
    custodia_url = (
        f"{settings.OPTIMUS_API_BASE_URL}/api/CuentaInversion/consultarSaldos"
    )
    custodia_headers = {
        "accept": "application/json",
        "X-SESSION-TOKEN": optimusToken,
        "Content-Type": "application/json",
    }

    custodia_data = {
        "IdEmpresa": 0,
        "IdUsuario": "string",
        "ClaveUsuario": "string",
        "CuentaInversion": [
            {
                "IdInterno": 0,
                "Filtro": "DocumentoIdentidad",
                "Valor": documento_identidad,
            },
            {
                "IdInterno": 0,
                "Filtro": "FechaInicioConsulta",
                "Valor": datetime.now().strftime("%Y-%m-%d"),
            },
            {
                "IdInterno": 0,
                "Filtro": "FechaTerminoConsulta",
                "Valor": datetime.now().strftime("%Y-%m-%d"),
            },
        ],
    }

    try:
        api_response = requests.post(
            custodia_url, headers=custodia_headers, json=custodia_data
        )
        api_response.raise_for_status()

        data = api_response.json()
    except requests.exceptions.RequestException as e:
        raise APIException(e)

    cuenta_filtrada = [
        cuenta
        for cuenta in data["CuentaInversion"]
        if cuenta["CodigoPortafolio"] == str(codigo_portafolio)
        and cuenta["CodigoMoneda"] == moneda
    ]

    saldo_disponible = cuenta_filtrada[0]["Saldo"]

    if saldo_disponible < monto:
        raise ValidationError(
            (
                f"Saldo insuficiente. Saldo disponible: "
                f"{str(round(saldo_disponible, 2))} {moneda}, "
                f"Costo total: {str(monto)} {moneda}"
            )
        )
