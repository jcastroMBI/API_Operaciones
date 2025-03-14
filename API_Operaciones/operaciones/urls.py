from django.urls import path
from .views import (
    CalculoComision,
    ConsultarInstrumento,
    ConsultarFichaCliente,
    ConsultarComprobantesFacturacion,
    ObtenerClienteAPIView,
)
from .custodia_views import (
    ConsultarCustodia,
    ConsultarMovimientosCustodia,
    ConsultarFlujoCustodia,
    ConsultarBalanceCustodia,
    ConsultarCartera,
    ConsultarEventosCapital,
    ConsultarEventosCapitalCliente,
)
from .cuenta_inversion_views import (
    consultarSaldos,
    ConsultarMovimientos,
    ConsultarFlujoCaja,
    ConsultarHistorialMovimientos,
)

urlpatterns = [
    ########################################## CUSTODIA ###########################################
    path(
        "Custodia/consultarCustodia/<str:documento_identidad>/<int:codigo_portafolio>/",
        ConsultarCustodia.as_view(),
        name="custodia",
    ),
    path(
        "Custodia/consultarMovimientos/<str:documento_identidad>/<str:moneda>/<str:fecha_inicio>/<str:fecha_termino>",
        ConsultarMovimientosCustodia.as_view(),
        name="movimientosCustodia",
    ),
    path(
        "Custodia/ConsultaFlujoCustodia/<str:documento_identidad>/<str:codigo_portafolio>/<str:nemotecnico>/<str:tipo_flujo>/<str:fecha_consulta>",
        ConsultarFlujoCustodia.as_view(),
        name="flujoCustodia",
    ),
    path(
        "Custodia/consultarBalanceCustodia/<str:documento_identidad>/<str:codigo_portafolio>/<str:fecha_consulta>",
        ConsultarBalanceCustodia.as_view(),
        name="balanceCustodia",
    ),
    path(
        "Custodia/consultarCartera/<str:documento_identidad>/<str:codigo_portafolio>/<str:fecha_consulta>",
        ConsultarCartera.as_view(),
        name="cartera",
    ),
    path(
        "Custodia/consultarEventosCapital/<str:instrumento>/<str:fecha_inicio>/<str:fecha_termino>",
        ConsultarEventosCapital.as_view(),
        name="eventosCapital",
    ),
    path(
        "Custodia/consultarEventosCapitalCliente/<str:documento_identidad>",
        ConsultarEventosCapitalCliente.as_view(),
        name="eventosCapitalCliente",
    ),
    ###################################### CUENTA INVERSION #######################################
    path(
        "CuentaInversion/consultarSaldos/<str:documento_identidad>/<int:codigo_portafolio>/",
        consultarSaldos.as_view(),
        name="saldos",
    ),
    path(
        "CuentaInversion/consultarMovimientos/<str:documento_identidad>/<int:codigo_portafolio>/<str:moneda>/<str:fecha_inicio>/<str:fecha_termino>",
        ConsultarMovimientos.as_view(),
        name="movimientos",
    ),
    path(
        "CuentaInversion/consultarFlujoCaja/<str:documento_identidad>/<str:codigo_portafolio>/<str:liquidacion>/<str:moneda>/<str:uso_flujo_caja>/<str:fecha_inicio>/<str:fecha_termino>",
        ConsultarFlujoCaja.as_view(),
        name="flujoCaja",
    ),
    path(
        "CuentaInversion/consultarHistorialMovimientos/<str:documento_identidad>/<str:codigo_portafolio>/<str:moneda>/<str:fecha_inicio>/<str:fecha_termino>",
        ConsultarHistorialMovimientos.as_view(),
        name="historialMovimientos",
    ),
    ########################################## CLIENTES ###########################################
    path(
        "Clientes/consultarFichaCliente/<str:documento_identidad>/<int:codigo_portafolio>/",
        ConsultarFichaCliente.as_view(),
        name="portafolio",
    ),
    path(
        "Clientes/consultarClientes/",
        ObtenerClienteAPIView.as_view(),
        name="portafolio",
    ),
    ######################################### PORTAFOLIO ##########################################
    path(
        "Portafolio/consultarCobros/<str:documento_identidad>/<int:codigo_portafolio>/<str:tipo_instrumento>",
        CalculoComision.as_view(),
        name="cobros",
    ),
    ######################################### PLATAFORMA ##########################################
    path(
        "Plataforma/consultarPrecioInstrumentos/<str:nombre_instrumento>/",
        ConsultarInstrumento.as_view(),
        name="instrumentos",
    ),
    ######################################### FACTURACION #########################################
    path(
        "Facturacion/consultarComprobantes/<str:documento_identidad>/<str:codigo_portafolio>/<str:fecha_inicio>/<str:fecha_termino>",
        ConsultarComprobantesFacturacion.as_view(),
        name="comprobantesFacturacion",
    ),
]
