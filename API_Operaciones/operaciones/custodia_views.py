import requests

from django.conf import settings
from django.utils import timezone

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .serializers import (
    CustodiaSerializer,
)
from .custodia_extensions import (
    consultar_balance_custodia_schema,
    consultar_cartera_schema,
    consultar_custodia_schema,
    consultar_eventos_capital_cliente_schema,
    consultar_eventos_capital_schema,
    consultar_flujo_custodia_schema,
    consultar_movimientos_schema,
)

from utils.cache import llamadas_restantes, usar_llamadas
from utils.optimus import obtener_token_optimus
from utils.validations import cliente_pertenece_agente


class ConsultarCustodia(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustodiaSerializer(many=True)

    @consultar_custodia_schema
    def get(self, request, documento_identidad, codigo_portafolio):
        ############################### Validación llamadas diarias ###############################
        if not request.user.is_staff:
            user_id = request.user.id
            remaining_calls = llamadas_restantes(user_id)

            if remaining_calls < 0:
                return Response(
                    {"error": "Has alcanzado el límite diario de llamadas a la API."},
                    status=429,
                )

        ########################## Validación cliente asignado a usuario ##########################
        if not request.user.is_staff:
            if not cliente_pertenece_agente(
                [request.user.codigoagente], documento_identidad
            ):
                return Response(
                    {"error": "No tienes permiso para consultar este cliente."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        ################################ Obtener token de optimus #################################
        try:
            optimusToken = obtener_token_optimus()
        except APIException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        ############################### Obtener custodia de optimus ###############################
        try:
            custodia_url = (
                f"{settings.OPTIMUS_API_BASE_URL}/api/Custodia/consultarCustodia"
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
                "Custodia": [
                    {
                        "IdInterno": 0,
                        "FechaConsulta": timezone.now().strftime("%Y-%m-%d"),
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

            api_response = requests.post(
                custodia_url, headers=custodia_headers, json=custodia_data
            )
            api_response.raise_for_status()
            if not request.user.is_staff:
                usar_llamadas(user_id, 1)
            data = api_response.json()
            lista = data["Custodia"]
            serializer = CustodiaSerializer(lista, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error en la consulta de custodia: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ConsultarMovimientosCustodia(APIView):
    permission_classes = [IsAuthenticated]

    @consultar_movimientos_schema
    def get(self, request, documento_identidad, moneda, fecha_inicio, fecha_termino):
        ########################## Validación cliente asignado a usuario ##########################
        if not request.user.is_staff:
            if not cliente_pertenece_agente(
                [request.user.codigoagente], documento_identidad
            ):
                return Response(
                    {"error": "No tienes permiso para operar este cliente."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        ############################### Validación llamadas diarias ###############################
        if not request.user.is_staff:
            user_id = request.user.id
            remaining_calls = llamadas_restantes(user_id)

            if remaining_calls < 0:
                return Response(
                    {"error": "Has alcanzado el límite diario de llamadas a la API."},
                    status=429,
                )

        ################################ Obtener token de optimus #################################
        try:
            optimusToken = obtener_token_optimus()
        except APIException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        #################################### Consultar Optimus ####################################
        movimientos_url = (
            f"{settings.OPTIMUS_API_BASE_URL}/api/Custodia/consultarMovimientos"
        )

        movimientos_headers = {
            "accept": "application/json",
            "X-SESSION-TOKEN": optimusToken,
            "Content-Type": "application/json",
        }

        movimientos_data = {
            "IdEmpresa": 1,
            "IdUsuario": "",
            "ClaveUsuario": "",
            "FiltrosConsulta": [
                {
                    "IdInterno": 0,
                    "Filtro": "DocumentoIdentidad",
                    "Valor": documento_identidad,
                },
                {"IdInterno": 0, "Filtro": "IdMoneda", "Valor": moneda},
                {"IdInterno": 0, "Filtro": "FechaDesde", "Valor": fecha_inicio},
                {"IdInterno": 0, "Filtro": "FechaHasta", "Valor": fecha_termino},
            ],
        }

        try:
            api_response = requests.post(
                movimientos_url, headers=movimientos_headers, json=movimientos_data
            )
            if not request.user.is_staff:
                usar_llamadas(user_id, 1)
            api_response.raise_for_status()

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error en la consulta de custodia: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(api_response.json(), status=status.HTTP_200_OK)


class ConsultarFlujoCustodia(APIView):
    permission_classes = [IsAuthenticated]

    @consultar_flujo_custodia_schema
    def get(
        self,
        request,
        documento_identidad,
        codigo_portafolio,
        nemotecnico,
        tipo_flujo,
        fecha_consulta,
    ):
        ########################## Validación cliente asignado a usuario ##########################
        if not request.user.is_staff:
            if not cliente_pertenece_agente(
                [request.user.codigoagente], documento_identidad
            ):
                return Response(
                    {"error": "No tienes permiso para operar este cliente."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        ############################### Validación llamadas diarias ###############################
        if not request.user.is_staff:
            user_id = request.user.id
            remaining_calls = llamadas_restantes(user_id)

            if remaining_calls < 0:
                return Response(
                    {"error": "Has alcanzado el límite diario de llamadas a la API."},
                    status=429,
                )

        ################################ Obtener token de optimus #################################
        try:
            optimusToken = obtener_token_optimus()
        except APIException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        #################################### Consultar Optimus ####################################
        historial_url = (
            f"{settings.OPTIMUS_API_BASE_URL}/api/Custodia/ConsultaFlujoCustodia"
        )

        historial_headers = {
            "accept": "application/json",
            "X-SESSION-TOKEN": optimusToken,
            "Content-Type": "application/json",
        }

        historial_data = {
            "IdEmpresa": 0,
            "IdUsuario": "",
            "ClaveUsuario": "",
            "FechaSaldo": fecha_consulta,
            "IdModulo": "PLA",
            "DiasProyeccion": 0,
            "IdBoveda": "DCV",
            "CodigoPortafolio": codigo_portafolio,
            "Custodia": [
                {
                    "Nemotecnico": nemotecnico,
                    "IdTipoFlujo": tipo_flujo,  ##FLJORD
                    "IdInterno": 0,
                    "FechaConsulta": fecha_consulta,
                    "Filtro": "DocumentoIdentidad",
                    "Valor": documento_identidad,
                }
            ],
        }

        try:
            api_response = requests.post(
                historial_url, headers=historial_headers, json=historial_data
            )
            if not request.user.is_staff:
                usar_llamadas(user_id, 1)
            api_response.raise_for_status()

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error en la consulta de custodia: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(api_response.json(), status=status.HTTP_200_OK)


class ConsultarBalanceCustodia(APIView):
    permission_classes = [IsAuthenticated]

    @consultar_balance_custodia_schema
    def get(self, request, documento_identidad, codigo_portafolio, fecha_consulta):
        ########################## Validación cliente asignado a usuario ##########################
        if not request.user.is_staff:
            if not cliente_pertenece_agente(
                [request.user.codigoagente], documento_identidad
            ):
                return Response(
                    {"error": "No tienes permiso para operar este cliente."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        ############################### Validación llamadas diarias ###############################
        if not request.user.is_staff:
            user_id = request.user.id
            remaining_calls = llamadas_restantes(user_id)

            if remaining_calls < 0:
                return Response(
                    {"error": "Has alcanzado el límite diario de llamadas a la API."},
                    status=429,
                )

        ################################ Obtener token de optimus #################################
        try:
            optimusToken = obtener_token_optimus()
        except APIException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        #################################### Consultar Optimus ####################################
        balance_url = (
            f"{settings.OPTIMUS_API_BASE_URL}/api/Custodia/consultarBalanceCustodia"
        )

        balance_headers = {
            "accept": "application/json",
            "X-SESSION-TOKEN": optimusToken,
            "Content-Type": "application/json",
        }

        balance_data = {
            "IdEmpresa": 0,
            "IdUsuario": "",
            "ClaveUsuario": "",
            "DocumentoIdentidad": documento_identidad,
            "CodigoPortafolio": codigo_portafolio,
            "FechaConsulta": fecha_consulta,
            "IncluyeCuentaInversion": "S",
        }

        try:
            api_response = requests.post(
                balance_url, headers=balance_headers, json=balance_data
            )
            if not request.user.is_staff:
                usar_llamadas(user_id, 1)
            api_response.raise_for_status()

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error en la consulta de custodia: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(api_response.json(), status=status.HTTP_200_OK)


class ConsultarCartera(APIView):
    permission_classes = [IsAuthenticated]

    @consultar_cartera_schema
    def get(self, request, documento_identidad, codigo_portafolio, fecha_consulta):
        ########################## Validación cliente asignado a usuario ##########################
        if not request.user.is_staff:
            if not cliente_pertenece_agente(
                [request.user.codigoagente], documento_identidad
            ):
                return Response(
                    {"error": "No tienes permiso para operar este cliente."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        ############################### Validación llamadas diarias ###############################
        if not request.user.is_staff:
            user_id = request.user.id
            remaining_calls = llamadas_restantes(user_id)

            if remaining_calls < 0:
                return Response(
                    {"error": "Has alcanzado el límite diario de llamadas a la API."},
                    status=429,
                )

        ################################ Obtener token de optimus #################################
        try:
            optimusToken = obtener_token_optimus()
        except APIException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        #################################### Consultar Optimus ####################################
        cartera_url = f"{settings.OPTIMUS_API_BASE_URL}/api/Custodia/consultarCartera"

        cartera_headers = {
            "accept": "application/json",
            "X-SESSION-TOKEN": optimusToken,
            "Content-Type": "application/json",
        }

        cartera_data = {
            "IdEmpresa": 0,
            "IdUsuario": "",
            "ClaveUsuario": "",
            "Carteras": [
                {"IdInterno": 0, "Filtro": "FechaConsulta", "Valor": fecha_consulta},
                {
                    "IdInterno": 0,
                    "Filtro": "DocumentoIdentidad",
                    "Valor": documento_identidad,
                },
                {
                    "IdInterno": 0,
                    "Filtro": "CodigoPortafolio",
                    "Valor": codigo_portafolio,
                },
            ],
        }

        try:
            api_response = requests.post(
                cartera_url, headers=cartera_headers, json=cartera_data
            )
            if not request.user.is_staff:
                usar_llamadas(user_id, 1)
            api_response.raise_for_status()

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error en la consulta de custodia: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(api_response.json(), status=status.HTTP_200_OK)


class ConsultarEventosCapital(APIView):
    permission_classes = [IsAuthenticated]

    @consultar_eventos_capital_schema
    def get(self, request, instrumento, fecha_inicio, fecha_termino):
        ############################### Validación llamadas diarias ###############################
        if not request.user.is_staff:
            user_id = request.user.id
            remaining_calls = llamadas_restantes(user_id)

            if remaining_calls < 0:
                return Response(
                    {"error": "Has alcanzado el límite diario de llamadas a la API."},
                    status=429,
                )

        ################################ Obtener token de optimus #################################
        try:
            optimusToken = obtener_token_optimus()
        except APIException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        #################################### Consultar Optimus ####################################
        eventos_url = (
            f"{settings.OPTIMUS_API_BASE_URL}/api/Custodia/consultarEventosCapital"
        )

        eventos_headers = {
            "accept": "application/json",
            "X-SESSION-TOKEN": optimusToken,
            "Content-Type": "application/json",
        }

        eventos_data = {
            "IdEmpresa": 0,
            "IdUsuario": "",
            "ClaveUsuario": "",
            "Custodia": [
                {"IdInterno": 0, "Filtro": "Instrumento", "Valor": instrumento},
                {"IdInterno": 0, "Filtro": "FechaLimiteInicio", "Valor": fecha_inicio},
                {
                    "IdInterno": 0,
                    "Filtro": "FechaLimiteTermino",
                    "Valor": fecha_termino,
                },
                {"IdInterno": 0, "Filtro": "FechaPagoInicio", "Valor": fecha_inicio},
                {"IdInterno": 0, "Filtro": "FechaPagoTermino", "Valor": fecha_termino},
            ],
        }

        try:
            api_response = requests.post(
                eventos_url, headers=eventos_headers, json=eventos_data
            )
            if not request.user.is_staff:
                usar_llamadas(user_id, 1)
            api_response.raise_for_status()

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error en la consulta de custodia: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(api_response.json(), status=status.HTTP_200_OK)


class ConsultarEventosCapitalCliente(APIView):
    permission_classes = [IsAuthenticated]

    @consultar_eventos_capital_cliente_schema
    def get(self, request, documento_identidad):
        ########################## Validación cliente asignado a usuario ##########################
        if not request.user.is_staff:
            if not cliente_pertenece_agente(
                [request.user.codigoagente], documento_identidad
            ):
                return Response(
                    {"error": "No tienes permiso para operar este cliente."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        ############################### Validación llamadas diarias ###############################
        if not request.user.is_staff:
            user_id = request.user.id
            remaining_calls = llamadas_restantes(user_id)

            if remaining_calls < 0:
                return Response(
                    {"error": "Has alcanzado el límite diario de llamadas a la API."},
                    status=429,
                )

        ################################ Obtener token de optimus #################################
        try:
            optimusToken = obtener_token_optimus()
        except APIException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        #################################### Consultar Optimus ####################################
        eventos_url = f"{settings.OPTIMUS_API_BASE_URL}/api/Custodia/consultarEventosCapitalCliente"

        eventos_headers = {
            "accept": "application/json",
            "X-SESSION-TOKEN": optimusToken,
            "Content-Type": "application/json",
        }

        eventos_data = {
            "IdEmpresa": 1,
            "IdUsuario": "",
            "ClaveUsuario": "",
            "Custodia": [
                {
                    "IdInterno": 0,
                    "Filtro": "DocumentoIdentidad",
                    "Valor": documento_identidad,
                }
            ],
        }

        try:
            api_response = requests.post(
                eventos_url, headers=eventos_headers, json=eventos_data
            )
            if not request.user.is_staff:
                usar_llamadas(user_id, 1)
            api_response.raise_for_status()

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error en la consulta de custodia: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(api_response.json(), status=status.HTTP_200_OK)
