from drf_spectacular.utils import extend_schema


def consultar_custodia_schema(func):
    return extend_schema(
        description="Obtiene una lista de la custodia de un cliente.", tags=["Custodia"]
    )(func)


from drf_spectacular.utils import extend_schema


def consultar_movimientos_schema(func):
    return extend_schema(
        tags=["Custodia"],
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
                                "IdInterno": {"type": "integer"},
                                "IdMovimiento": {"type": "integer"},
                                "Nominal": {"type": "string"},
                                "Estado": {"type": "string"},
                                "IdTipoDocumentoIdentidad": {"type": "string"},
                                "CodigoPortafolio": {"type": "string"},
                                "FechaOperacion": {"type": "string"},
                                "FechaLiquidacion": {"type": "string"},
                                "Operacion": {"type": "string"},
                                "Concepto": {"type": "string"},
                                "Instrumento": {"type": "string"},
                                "IdCondicionDeLiquidacion": {"type": "string"},
                                "Cantidad": {"type": "integer"},
                                "IdMoneda": {"type": "string"},
                                "MontoMonedaInstrumento": {"type": "integer"},
                                "DocumentoIdentidad": {"type": "string"},
                                "NombreCompleto": {"type": "string"},
                                "IdTipoReajuste": {"type": "string"},
                                "Precio": {"type": "integer"},
                                "MontoMonedaLocal": {"type": "integer"},
                                "Boveda": {"type": "string"},
                                "IdMatrizAgrupador": {"type": "integer"},
                                "NemoSVS": {"type": "string"},
                            },
                        },
                    },
                },
            }
        },
    )(func)


from drf_spectacular.utils import extend_schema


def consultar_flujo_custodia_schema(func):
    return extend_schema(
        tags=["Custodia"],
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
                    "Custodia": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "FechaCustodia": {"type": "string"},
                                "IdClasificacionTipoInstrumento": {"type": "string"},
                                "NombreClasificacionTipoInstrumento": {
                                    "type": "string"
                                },
                                "IdTipoInstrumento": {"type": "string"},
                                "NombreTipoInstrumento": {"type": "string"},
                                "ISIN": {"type": "string"},
                                "IdInstrumento": {"type": "integer"},
                                "NombreInstrumento": {"type": "string"},
                                "IdEmisor": {"type": "string"},
                                "EsFungible": {"type": "string"},
                                "IdPortafolio": {"type": "integer"},
                                "DocumentoIdentidad": {"type": "string"},
                                "NombreCliente": {"type": "string"},
                                "CodigoPortafolio": {"type": "string"},
                                "IdBoveda": {"type": "string"},
                                "NumeroCuentaBoveda": {"type": "string"},
                                "IdMonedaPrincipal": {"type": "string"},
                                "SaldoCustodia": {"type": "integer"},
                                "FechaVencimiento": {"type": "string"},
                                "CodigoTipoCuenta": {"type": "string"},
                                "TipoAhorro": {"type": "string"},
                                "TipoCuenta": {"type": "string"},
                                "IdRegimenTributario": {"type": "string"},
                                "IdMatrizAgrupador": {"type": "integer"},
                                "IdSerieFondo": {"type": "string"},
                                "IdTipoFlujo": {"type": "string"},
                            },
                        },
                    },
                },
            }
        },
    )(func)


def consultar_balance_custodia_schema(func):
    return extend_schema(
        tags=["Custodia"],
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
                    "Balance": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "ClasificacionTipoInstrumento": {"type": "string"},
                                "IdClasificacionTipoInstrumento": {"type": "string"},
                                "TipoInstrumento": {"type": "string"},
                                "IdTipoInstrumento": {"type": "string"},
                                "Activo": {"type": "integer"},
                                "Pasivo": {"type": "integer"},
                                "Saldo": {"type": "integer"},
                                "Rentabilidad": {"type": "integer"},
                            },
                        },
                    },
                },
            }
        },
    )(func)


from drf_spectacular.utils import extend_schema


def consultar_cartera_schema(func):
    return extend_schema(
        tags=["Custodia"],
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
                    "Carteras": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "IdInterno": {"type": "integer"},
                                "IdCartera": {"type": "integer"},
                                "FechaCompra": {"type": "string"},
                                "Nemotecnico": {"type": "string"},
                                "Cantidad": {"type": "integer"},
                                "PrecioCompra": {"type": "integer"},
                                "PrecioMercado": {"type": "integer"},
                                "MontoCompro": {"type": "integer"},
                                "MontoMercado": {"type": "integer"},
                                "IdMoneda": {"type": "string"},
                                "IdTipoInstrumento": {"type": "string"},
                                "IdClasificacionTipoInstrumento": {"type": "string"},
                            },
                        },
                    },
                },
            }
        },
    )(func)


def consultar_eventos_capital_schema(func):
    return extend_schema(
        tags=["Custodia"],
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
                    "Resultado": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "IdInterno": {"type": "integer"},
                                "TipoEvento": {"type": "string"},
                                "NumeroDividendo": {"type": "integer"},
                                "SecuenciaEvento": {"type": "integer"},
                                "Descripcion": {"type": "string"},
                                "IdClasificacionTipoInstrumento": {"type": "integer"},
                                "TipoInstrumento": {"type": "string"},
                                "Nemo": {"type": "string"},
                                "ISIN": {"type": "string"},
                                "FechaActualizacion": {"type": "string"},
                                "FechaLimite": {"type": "string"},
                                "FechaPago": {"type": "string"},
                                "Boveda": {"type": "integer"},
                                "IdMoneda": {"type": "string"},
                                "Moneda": {"type": "integer"},
                                "MontoRepartido": {"type": "string"},
                                "ISFUT": {"type": "string"},
                                "TasaEfectiva": {"type": "string"},
                                "AccionesAntiguas": {"type": "integer"},
                                "Paridad": {"type": "integer"},
                                "InstrumentoNuevo": {"type": "string"},
                                "AccionesNuevas": {"type": "string"},
                                "NumeroDvidendo": {"type": "integer"},
                                "TipoDividendo": {"type": "string"},
                                "Inscrito": {"type": "string"},
                                "Estado": {"type": "string"},
                                "Emisor": {"type": "string"},
                            },
                        },
                    },
                },
            }
        },
    )(func)


def consultar_eventos_capital_cliente_schema(func):
    return extend_schema(
        tags=["Custodia"],
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
                    "Resultado": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "IdInterno": {"type": "integer"},
                                "IdEventoCapital": {"type": "string"},
                                "TipoEvento": {"type": "string"},
                                "NumeroDividendo": {"type": "integer"},
                                "SecuenciaEvento": {"type": "integer"},
                                "TipoSocioNegocio": {"type": "string"},
                                "TipoInstrumento": {"type": "string"},
                                "CodigoPortafolio": {"type": "string"},
                                "CodigoClasificacionTipoInstrumento": {
                                    "type": "string"
                                },
                                "Nemo": {"type": "string"},
                                "ISIN": {"type": "string"},
                                "NemoNuevo": {"type": "string"},
                                "TipoCartera": {"type": "string"},
                                "RUT": {"type": "string"},
                                "NombreCliente": {"type": "string"},
                                "MontoCapital": {"type": "integer"},
                                "Precio": {"type": "integer"},
                                "AccionesAntiguas": {"type": "integer"},
                                "AccionesNuevas": {"type": "string"},
                                "PrecioNuevo": {"type": "integer"},
                                "CantidadNueva": {"type": "integer"},
                                "MontoInteres": {"type": "integer"},
                                "MontoReajuste": {"type": "integer"},
                                "CantidadDerecho": {"type": "integer"},
                                "Total": {"type": "integer"},
                                "MontoRetenido": {"type": "integer"},
                                "Moneda": {"type": "string"},
                                "FechaMaterializacionPago": {"type": "string"},
                                "Agente": {"type": "string"},
                                "Nombre": {"type": "string"},
                                "Boveda": {"type": "string"},
                                "Estado": {"type": "string"},
                                "MedioPago": {"type": "string"},
                                "TipoCuentaBoveda": {"type": "string"},
                                "NumeroCuentaBoveda": {"type": "integer"},
                                "Paga": {"type": "string"},
                                "TipoReajuste": {"type": "string"},
                                "MntoInteres": {"type": "integer"},
                                "Amortizacion": {"type": "integer"},
                                "AfectoClearing": {"type": "string"},
                                "ProcesadoClearing": {"type": "string"},
                                "Regimen": {"type": "string"},
                                "ISFUT": {"type": "string"},
                                "RetencionISFUT": {"type": "string"},
                            },
                        },
                    },
                },
            }
        },
    )(func)
