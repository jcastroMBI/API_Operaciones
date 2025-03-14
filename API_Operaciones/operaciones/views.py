from datetime import date
from django.db import connections
import requests

from django.conf import settings

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    ClienteSerializer,
)
from .extensions import (
    consultar_cobros_schema,
    obtener_cliente_schema,
    consultar_comprobante_facturacion_schema,
    consultar_ficha_cliente_schema,
)

from utils.cache import llamadas_restantes, usar_llamadas
from utils.optimus import obtener_token_optimus
from utils.validations import cliente_pertenece_agente


class CalculoComision(APIView):
    permission_classes = [IsAuthenticated]

    @consultar_cobros_schema
    def get(self, request, documento_identidad, codigo_portafolio, tipo_instrumento):
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

        cobros_url = f"{settings.OPTIMUS_API_BASE_URL}/api/Portafolio/consultarCobros"

        cobros_headers = {
            "accept": "application/json",
            "X-SESSION-TOKEN": optimusToken,
            "Content-Type": "application/json",
        }

        cobros_data = {
            "IdEmpresa": 0,
            "IdUsuario": "string",
            "ClaveUsuario": "string",
            "Portafolios": [
                {
                    "IdInterno": 0,
                    "Filtro": "DocumentoIdentidad",
                    "Valor": documento_identidad,
                },
                {
                    "IdInterno": 0,
                    "Filtro": "CodigoPortafolio",
                    "Valor": str(codigo_portafolio),
                },
            ],
        }

        try:
            api_response = requests.post(
                cobros_url, headers=cobros_headers, json=cobros_data
            )
            if not request.user.is_staff:
                usar_llamadas(user_id, 1)
            api_response.raise_for_status()

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error en la consulta de custodia: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cobros_result = api_response.json().get("Cobros", [])

        tipo_producto_esperado = {
            "ACN": "INAC",
            "CFI": "INCI",
            "ETN": "INEN",
        }.get(tipo_instrumento)

        # Filtrar los cobros según el tipo de producto esperado
        cobros_filtrados = [
            cobro
            for cobro in cobros_result
            if cobro.get("IdTipoProducto") == tipo_producto_esperado
        ]

        cobros_dict = {}

        for cobro in cobros_filtrados:
            id_cobro = cobro.get("IdCobro")
            canal_ingreso = cobro.get("CanalIngreso", "TODOS")
            valor_cobro = str(cobro.get("ValorCobro"))

            if canal_ingreso == "CLIENTE":
                continue

            # Si el IdCobro ya está en el diccionario, priorizar "Agente"
            if id_cobro in cobros_dict:
                # Si el canal actual es "Agente", reemplazar el valor existente
                if canal_ingreso == "AGENTE":
                    cobros_dict[id_cobro] = valor_cobro
            else:
                # Agregar el registro si aún no existe
                cobros_dict[id_cobro] = valor_cobro

        return Response(cobros_dict, status=status.HTTP_200_OK)


class ConsultarInstrumento(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, nombre_instrumento):
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
        instrumento_url = f"{settings.OPTIMUS_API_BASE_URL}/api/Plataforma/consultarPrecioInstrumentos"
        instrumento_headers = {
            "accept": "application/json",
            "X-SESSION-TOKEN": optimusToken,
            "Content-Type": "application/json",
        }

        instrumento_data = {
            "IdEmpresa": 1,
            "IdUsuario": "string",
            "ClaveUsuario": "string",
            "SoloInscritos": "S",
            "Instrumentos": [
                {
                    "IdInterno": 0,
                    "Filtro": "NombreInstrumento",
                    "Valor": nombre_instrumento,
                },
                {"IdInterno": 0, "Filtro": "Bolsa", "Valor": "BCS"},
                {
                    "IdInterno": 0,
                    "Filtro": "ClasificacionTipoInstrumento",
                    "Valor": "RV",
                },
                {"IdInterno": 0, "Filtro": "Fecha", "Valor": date.today().isoformat()},
            ],
        }

        try:
            api_response = requests.post(
                instrumento_url, headers=instrumento_headers, json=instrumento_data
            )
            if not request.user.is_staff:
                usar_llamadas(user_id, 1)
            api_response.raise_for_status()

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error en la consulta de custodia: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        instrumentos_result = api_response.json().get("Instrumentos", [])
        instrumento = instrumentos_result[0]

        return Response(instrumento, status=status.HTTP_200_OK)


class ConsultarFichaCliente(APIView):
    permission_classes = [IsAuthenticated]

    @consultar_ficha_cliente_schema
    def get(self, request, documento_identidad, codigo_portafolio):
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

        #################################### Buscar portafolios ###################################
        portafolio_url = (
            f"{settings.OPTIMUS_API_BASE_URL}/api/Clientes/consultarFichaCliente"
        )
        portafolio_headers = {
            "accept": "application/json",
            "X-SESSION-TOKEN": optimusToken,
            "Content-Type": "application/json",
        }

        portafolio_data = {
            "IdEmpresa": 0,
            "IdUsuario": "string",
            "ClaveUsuario": "string",
            "ClaveUsuario": "string",
            "Filtros": [
                {
                    "IdInterno": 0,
                    "Filtro": "DocumentoIdentidad",
                    "Valor": documento_identidad,
                }
            ],
        }

        try:
            api_response = requests.post(
                portafolio_url, headers=portafolio_headers, json=portafolio_data
            )
            if not request.user.is_staff:
                usar_llamadas(user_id, 1)
            api_response.raise_for_status()

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error en la consulta de custodia: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        portafolios_result = (
            api_response.json().get("SocioNegocio", [])[0].get("DatosPortafolios", [])
        )
        filtrados = [
            portafolio
            for portafolio in portafolios_result
            if portafolio["CodigoPortafolio"] == str(codigo_portafolio)
        ]

        return Response(filtrados[0], status=status.HTTP_200_OK)


class ConsultarComprobantesFacturacion(APIView):
    permission_classes = [IsAuthenticated]

    @consultar_comprobante_facturacion_schema
    def get(
        self,
        request,
        documento_identidad,
        codigo_portafolio,
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
        comprobantes_url = (
            f"{settings.OPTIMUS_API_BASE_URL}/api/Facturacion/consultarComprobantes"
        )

        comprobantes_headers = {
            "accept": "application/json",
            "X-SESSION-TOKEN": optimusToken,
            "Content-Type": "application/json",
        }

        comprobantes_data = {
            "IdEmpresa": 0,
            "IdUsuario": "",
            "ClaveUsuario": "",
            "DocumentoIdentidad": documento_identidad,
            "FechaInicial": fecha_inicio,
            "FechaFinal": fecha_termino,
            "Portafolios": [{"CodigoPortafolio": codigo_portafolio}],
            "TipoDocumento": [{"TipoDocumento": "FAE"}],
        }

        try:
            api_response = requests.post(
                comprobantes_url, headers=comprobantes_headers, json=comprobantes_data
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


class ObtenerClienteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClienteSerializer

    @obtener_cliente_schema
    def get(self, request):
        ################################# Consultar clientes en bd ################################
        try:
            query = """
                SELECT 
                    cli.Nombres AS nombre_cliente,
                    cli.ApellidoPaterno AS apellido_cliente,
                    cli.RazonSocial AS razon_social_cliente,
                    cli.IdDocumentoIdentidad AS documento_cliente,
                    cliper.DocumentoIdentidad AS documento_identidad_clipersona,
                    age.Nombres AS nombre_agente,
                    age.ApellidoPaterno AS apellido_agente,
                    age.RazonSocial AS razon_social_agente
                FROM 
                    [BCSMBI_ONLINE].[dbo].[SocioNegocio_Cliente] AS cli
                LEFT JOIN 
                    [BCSMBI_ONLINE].[dbo].[SocioNegocio_Persona] AS age 
                    ON cli.IdPersonaEjecutivo = age.IdPersona
                LEFT JOIN 
                    [BCSMBI_ONLINE].[dbo].[SocioNegocio_Persona] AS cliper 
                    ON cliper.IdDocumentoIdentidad = cli.IdDocumentoIdentidad
                WHERE 
                    cli.IdPersonaEjecutivo = %s;
            """

            with connections["bcsmbi_online"].cursor() as cursor:
                cursor.execute(query, [request.user.codigoagente])
                resultados = cursor.fetchall()

            ################################### Serializar data ###################################
            data = [
                {
                    "nombre_cliente": row[0],
                    "apellido_cliente": row[1],
                    "razon_social_cliente": row[2],
                    "documento_cliente": row[3],
                    "rut_cliente": row[4],
                    "nombre_agente": row[5],
                    "apellido_agente": row[6],
                    "razon_social_agente": row[7],
                }
                for row in resultados
            ]

            serializer = ClienteSerializer(data, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
