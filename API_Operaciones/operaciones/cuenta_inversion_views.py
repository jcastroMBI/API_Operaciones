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
    MovimientoSerializer,
    SaldoSerializer,
)
from .cuenta_inversion_extensions import (
    consultar_saldo_schema,
    consultar_movimientos_schema,
    consultar_flujo_caja_schema,
    consultar_historial_movimientos_schema,
)

from utils.cache import llamadas_restantes, usar_llamadas
from utils.optimus import obtener_token_optimus
from utils.validations import cliente_pertenece_agente


class consultarSaldos(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SaldoSerializer(many=True)

    @consultar_saldo_schema
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
                        "Valor": timezone.now().strftime("%Y-%m-%d"),
                    },
                    {
                        "IdInterno": 0,
                        "Filtro": "FechaTerminoConsulta",
                        "Valor": timezone.now().strftime("%Y-%m-%d"),
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

            # Filtrar cuentas donde CodigoPortafolio sea la ingresada
            cuentas_filtradas = [
                cuenta
                for cuenta in data["CuentaInversion"]
                if cuenta["CodigoPortafolio"] == str(codigo_portafolio)
            ]
            return Response(cuentas_filtradas, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error en la consulta de custodia: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ConsultarMovimientos(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MovimientoSerializer(many=True)

    @consultar_movimientos_schema
    def get(
        self,
        request,
        documento_identidad,
        codigo_portafolio,
        moneda,
        fecha_inicio,
        fecha_termino,
    ):
        ########################## Validación cliente asignado a usuario ##########################
        request = self.request
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

        ####################################### Rutear orden ######################################
        historial_url = (
            f"{settings.OPTIMUS_API_BASE_URL}/api/CuentaInversion/consultarMovimientos"
        )
        historial_headers = {
            "accept": "application/json",
            "X-SESSION-TOKEN": optimusToken,
            "Content-Type": "application/json",
        }

        # fecha_inicio = (datetime.now() - timedelta(days=30)).date().isoformat()
        # fecha_termino = datetime.now().date().isoformat()

        historial_data = {
            "IdEmpresa": 0,
            "IdUsuario": "string",
            "ClaveUsuario": "string",
            "TipoFechaConsulta": "string",
            "CuentaInversion": [
                {
                    "IdInterno": 0,
                    "Filtro": "FechaInicioConsulta",
                    "Valor": fecha_inicio,
                },
                {
                    "IdInterno": 0,
                    "Filtro": "FechaTerminoConsulta",
                    "Valor": fecha_termino,
                },
                {
                    "IdInterno": 0,
                    "Filtro": "DocumentoIdentidad",
                    "Valor": documento_identidad,
                },
                {"IdInterno": 0, "Filtro": "IdMoneda", "Valor": moneda},
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

        movimientos_result = api_response.json().get("CuentaInversion", [])
        filtrados = [
            movimiento
            for movimiento in movimientos_result
            if movimiento["CodigoPortafolio"] == str(codigo_portafolio)
        ]

        serializer = MovimientoSerializer(filtrados, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ConsultarFlujoCaja(APIView):
    permission_classes = [IsAuthenticated]

    @consultar_flujo_caja_schema
    def get(
        self,
        request,
        documento_identidad,
        codigo_portafolio,
        liquidacion,
        moneda,
        fecha_inicio,
        fecha_termino,
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
        flujocaja_url = (
            f"{settings.OPTIMUS_API_BASE_URL}/api/CuentaInversion/consultarFlujoCaja"
        )

        flujocaja_headers = {
            "accept": "application/json",
            "X-SESSION-TOKEN": optimusToken,
            "Content-Type": "application/json",
        }

        flujocaja_data = {
            "IdEmpresa": 0,
            "IdUsuario": "",
            "ClaveUsuario": "",
            "Portafolios": [
                {
                    "IdInterno": 0,
                    "Filtro": "DocumentoIdentidad",
                    "Valor": documento_identidad,
                    "IdMoneda": moneda,
                    "FechaInicioConsulta": fecha_inicio,
                    "FechaTerminoConsulta": fecha_termino,
                },
                {
                    "IdInterno": 0,
                    "Filtro": "CodigoPortafolio",
                    "Valor": codigo_portafolio,
                    "IdMoneda": moneda,
                    "FechaInicioConsulta": fecha_inicio,
                    "FechaTerminoConsulta": fecha_termino,
                },
                {
                    "IdInterno": 0,
                    "Filtro": "CondicionLiquidacion",
                    "Valor": liquidacion,
                    "IdMoneda": moneda,
                    "FechaInicioConsulta": fecha_inicio,
                    "FechaTerminoConsulta": fecha_termino,
                },
                {
                    "IdInterno": 0,
                    "Filtro": "UsoFlujoCaja",
                    "Valor": "CUENTA_INVERSION",
                    "IdMoneda": moneda,
                    "FechaInicioConsulta": fecha_inicio,
                    "FechaTerminoConsulta": fecha_termino,
                },
            ],
        }

        try:
            api_response = requests.post(
                flujocaja_url, headers=flujocaja_headers, json=flujocaja_data
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


class ConsultarHistorialMovimientos(APIView):
    permission_classes = [IsAuthenticated]

    @consultar_historial_movimientos_schema
    def get(
        self,
        request,
        documento_identidad,
        codigo_portafolio,
        moneda,
        fecha_inicio,
        fecha_termino,
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
        historial_url = f"{settings.OPTIMUS_API_BASE_URL}/api/CuentaInversion/consultarHistorialMovimientos"

        historial_headers = {
            "accept": "application/json",
            "X-SESSION-TOKEN": optimusToken,
            "Content-Type": "application/json",
        }

        historial_data = {
            "IdEmpresa": 0,
            "IdUsuario": "",
            "ClaveUsuario": "",
            "Portafolios": [
                {
                    "IdInterno": 0,
                    "Filtro": "DocumentoIdentidad",
                    "Valor": documento_identidad,
                },
                {
                    "IdInterno": 0,
                    "Filtro": "FechaInicioConsulta",
                    "Valor": fecha_inicio,
                },
                {
                    "IdInterno": 0,
                    "Filtro": "FechaTerminoConsulta",
                    "Valor": fecha_termino,
                },
                {
                    "IdInterno": 0,
                    "Filtro": "CodigoPortafolio",
                    "Valor": codigo_portafolio,
                },
                {"IdInterno": 0, "Filtro": "IdMoneda", "Valor": moneda},
                {"IdInterno": 0, "Filtro": "IdMatrizAgrupador", "Valor": "0"},
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
