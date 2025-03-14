from drf_spectacular.utils import extend_schema
from .serializers import CalculoComisionRequestSerializer


def consultar_saldo_schema(func):
    return extend_schema(
        description="Obtiene el saldo de un cliente.", tags=["Cuenta Inversion"]
    )(func)


def consultar_movimientos_schema(func):
    return extend_schema(
        request=CalculoComisionRequestSerializer,
        description=(
            "Muestra los movimientos de un cliente entre la fecha de inicio y la fecha de termino.\n\n"
            "**moneda:** `CLP`, `USD` o `EUR` \n\n"
            "**fechas:** AAAA-MM-DD \n"
        ),
        tags=["Cuenta Inversion"],
    )(func)


def consultar_flujo_caja_schema(func):
    return extend_schema(
        tags=["Cuenta Inversion"],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "ContadorErrores": {"type": "integer"},
                    "Mensajes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "IdInterno": {"type": "integer"},
                                "TipoMensaje": {"type": "string"},
                                "Codigo": {"type": "string"},
                                "Mensaje": {"type": "string"},
                            },
                        },
                    },
                    "SaldosPortafolio": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "FechaSaldo": {"type": "string"},
                                "IdPortafolio": {"type": "integer"},
                                "IdMoneda": {"type": "string"},
                                "Saldo": {"type": "integer"},
                            },
                        },
                    },
                },
            }
        },
    )(func)


from drf_spectacular.utils import extend_schema


def consultar_historial_movimientos_schema(func):
    return extend_schema(
        tags=["Cuenta Inversion"],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "ContadorErrores": {"type": "integer"},
                    "Mensajes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "IdInterno": {"type": "integer"},
                                "TipoMensaje": {"type": "string"},
                                "Codigo": {"type": "string"},
                                "Mensaje": {"type": "string"},
                            },
                        },
                    },
                    "Movimientos": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "IdCargoAbonoMovimiento": {"type": "integer"},
                                "NombreCliente": {"type": "string"},
                                "IdCliente": {"type": "integer"},
                                "IdPortafolio": {"type": "integer"},
                                "FechaMovimiento": {"type": "string"},
                                "FechaLiquidacion": {"type": "string"},
                                "IdMoneda": {"type": "string"},
                                "IdConcepto": {"type": "string"},
                                "NombreConcepto": {"type": "string"},
                                "Cargo": {"type": "integer"},
                                "Abono": {"type": "integer"},
                                "FolioComprobante": {"type": "string"},
                                "IdEstado": {"type": "string"},
                                "NombreEstado": {"type": "string"},
                                "NombreTipoComprobante": {"type": "string"},
                                "NombreTipoProducto": {"type": "string"},
                                "NombreTipoOperacion": {"type": "string"},
                                "NombreTipoMovimiento": {"type": "string"},
                                "SaldoSimulado": {"type": "integer"},
                                "CodigoPortafolio": {"type": "string"},
                                "IdComprobante": {"type": "integer"},
                                "IdRespuestaDTE": {"type": "integer"},
                                "RespuestaPdfDTE": {"type": "string"},
                                "DocumentoIdentidad": {"type": "string"},
                                "Origen": {"type": "string"},
                                "IdMatrizAgrupador": {"type": "integer"},
                                "EsADC": {"type": "string"},
                            },
                        },
                    },
                },
            }
        },
    )(func)
