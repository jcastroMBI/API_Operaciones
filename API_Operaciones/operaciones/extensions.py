from drf_spectacular.utils import extend_schema

from .serializers import ClienteSerializer


def consultar_cobros_schema(func):
    return extend_schema(
        description=(
            "Muestra los cobros de un cliente.\n\n"
            "**Tipo_Instrumento:** `ACN`, `ETN` o `CFI` "
        ),
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
                    "Cobros": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "IdInterno": {"type": "string"},
                                "IdPerfilCobros": {"type": "string"},
                                "CanalIngreso": {"type": "string"},
                                "CodigoCobroClasificacion": {"type": "string"},
                                "IdCobro": {"type": "string"},
                                "Mercado": {"type": "string"},
                                "IdTipoProducto": {"type": "string"},
                                "ValorCobro": {"type": "integer"},
                                "ValorTopeMinimoOrden": {"type": "integer"},
                                "IdTipoOperacion": {"type": "string"},
                            },
                        },
                    },
                },
            }
        },
    )(func)


def obtener_cliente_schema(func):
    return extend_schema(
        description="Obtiene la información de tus clientes, en base al token de autorización.",
        responses={200: ClienteSerializer(many=True)},
    )(func)


def consultar_ficha_cliente_schema(func):
    return extend_schema(
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
                    "SocioNegocio": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "IdPersona": {"type": "integer"},
                                "IdCliente": {"type": "integer"},
                                "TipoEntidad": {"type": "string"},
                                "TipoDocumentoIdentidad": {"type": "string"},
                                "DocumentoIdentidad": {"type": "string"},
                                "IdTipoPersona": {"type": "string"},
                                "TipoPersona": {"type": "string"},
                                "Nombres": {"type": "string"},
                                "ApellidoPaterno": {"type": "string"},
                                "ApellidoMaterno": {"type": "string"},
                                "RazonSocial": {"type": "string"},
                                "IdGenero": {"type": "string"},
                                "Genero": {"type": "string"},
                                "IdEstado": {"type": "string"},
                                "Estado": {"type": "string"},
                                "IdPaisNacimientoConstitucion": {"type": "integer"},
                                "PaisNacimientoConstitucion": {"type": "string"},
                                "IdTransparenciaFiscal": {"type": "string"},
                                "ResidenciaTributariaExtranjera": {"type": "string"},
                                "IdPaisResidenciaCasaMatriz": {"type": "integer"},
                                "PaisResidenciaCasaMatriz": {"type": "string"},
                                "IdPaisNacionalidad": {"type": "integer"},
                                "PaisNacionalidad": {"type": "string"},
                                "FechaNacimientoConstitucion": {"type": "string"},
                                "FechaDefuncion": {"type": "string"},
                                "FechaInicioActividad": {"type": "string"},
                                "GlobalLegalEntity": {"type": "string"},
                                "IdEstadoCivil": {"type": "string"},
                                "EstadoCivil": {"type": "string"},
                                "IdRegimenConyugal": {"type": "string"},
                                "RegimenConyugal": {"type": "string"},
                                "IdGiro": {"type": "integer"},
                                "Giro": {"type": "string"},
                                "IdProfesion": {"type": "string"},
                                "Profesion": {"type": "string"},
                                "IdCargo": {"type": "string"},
                                "Cargo": {"type": "string"},
                                "IdRangoPatrimonio": {"type": "integer"},
                                "RangoPatrimonio": {"type": "string"},
                                "IdTipoBloqueo": {"type": "string"},
                                "NombreTipoBloqueo": {"type": "string"},
                                "IdSituacionLaboral": {"type": "string"},
                                "CodigoRangoRenta": {"type": "string"},
                                "RangoRenta": {"type": "string"},
                                "CodigoRangoNivelVenta": {"type": "string"},
                                "RangoNivelVenta": {"type": "string"},
                                "CodigoPropositoTransaccion": {"type": "string"},
                                "PropositoTransaccion": {"type": "string"},
                                "TiposDocumento": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "IdDocumentoIdentidad": {"type": "integer"},
                                            "TipoDocumento": {"type": "string"},
                                            "NumeroDocumento": {"type": "string"},
                                            "NumeroSerie": {"type": "string"},
                                            "FechaEmision": {"type": "string"},
                                            "FechaVencimiento": {"type": "string"},
                                        },
                                    },
                                },
                                "CuentaBancaria": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "IdCuentaBancaria": {"type": "integer"},
                                            "NumeroCuentaBancaria": {"type": "string"},
                                            "IdEstado": {"type": "string"},
                                            "IdMoneda": {"type": "string"},
                                            "CodigoTipoCuentaBancaria": {
                                                "type": "string"
                                            },
                                            "TipoCuentaBancaria": {"type": "string"},
                                            "IdBanco": {"type": "integer"},
                                            "Banco": {"type": "string"},
                                            "IdPlaza": {"type": "string"},
                                            "NombrePlaza": {"type": "string"},
                                        },
                                    },
                                },
                                "TarjetaBancaria": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "IdTarjetaBancaria": {"type": "integer"},
                                            "IdBanco": {"type": "integer"},
                                            "Banco": {"type": "string"},
                                            "IdTipo": {"type": "string"},
                                            "Tipo": {"type": "string"},
                                            "NumeroTarjeta": {"type": "string"},
                                            "CodigoVerificacion": {"type": "integer"},
                                            "FechaVencimiento": {"type": "string"},
                                        },
                                    },
                                },
                                "Telefono": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "IdTelefono": {"type": "integer"},
                                            "IdProposito": {"type": "string"},
                                            "Proposito": {"type": "string"},
                                            "Numero": {"type": "string"},
                                            "IdPais": {"type": "integer"},
                                            "Pais": {"type": "string"},
                                            "Tipo": {"type": "string"},
                                            "Anexo": {"type": "string"},
                                        },
                                    },
                                },
                                "DireccionFisica": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "IdDireccionFisica": {"type": "integer"},
                                            "IdProposito": {"type": "string"},
                                            "Proposito": {"type": "string"},
                                            "Sector": {"type": "string"},
                                            "CodigoPostal": {"type": "string"},
                                            "IdComuna": {"type": "integer"},
                                            "Comuna": {"type": "string"},
                                            "Calle": {"type": "string"},
                                            "Numero": {"type": "string"},
                                            "Departamento": {"type": "string"},
                                            "Complemento": {"type": "string"},
                                            "IdCiudad": {"type": "integer"},
                                            "Ciudad": {"type": "string"},
                                        },
                                    },
                                },
                                "DireccionElectronica": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "IdDireccionElectronica": {
                                                "type": "integer"
                                            },
                                            "Tipo": {"type": "string"},
                                            "IdProposito": {"type": "string"},
                                            "Proposito": {"type": "string"},
                                            "Direccion": {"type": "string"},
                                            "IdEstado": {"type": "string"},
                                            "Estado": {"type": "string"},
                                        },
                                    },
                                },
                                "IndicadorPersona": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "ValorIndicador": {"type": "string"},
                                            "CodigoTipoIndicador": {"type": "string"},
                                            "GrupoIndicador": {"type": "string"},
                                        },
                                    },
                                },
                                "Relacion": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "IdPersonaRelacionada": {"type": "integer"},
                                            "IdTipoRelacion": {"type": "string"},
                                            "NombreTipoRelacion": {"type": "string"},
                                            "TipoDocumentoIdentidad": {
                                                "type": "string"
                                            },
                                            "DocumentoIdentidad": {"type": "string"},
                                            "NombreCompleto": {"type": "string"},
                                        },
                                    },
                                },
                                "NombreFantasia": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "IdNombreFantasia": {"type": "integer"},
                                            "Nombre": {"type": "string"},
                                            "IdEstado": {"type": "string"},
                                        },
                                    },
                                },
                                "FatcaCrs": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "IdClasificacionFatca": {"type": "string"},
                                            "NombreClasificacionFatca": {
                                                "type": "string"
                                            },
                                            "IdClasificacionEmpresaFatca": {
                                                "type": "string"
                                            },
                                            "NombreClasificacionEmpresaFatca": {
                                                "type": "string"
                                            },
                                            "NumeroGIIN": {"type": "string"},
                                            "FechaFirmaFormularioString": {
                                                "type": "string"
                                            },
                                            "AutorizacionInformarOrganismo": {
                                                "type": "string"
                                            },
                                            "NACEEUU": {"type": "string"},
                                            "NACEEUUExplicacion": {"type": "string"},
                                            "ObligacionesFiscales": {"type": "string"},
                                            "ObligacionesFiscalesExplicacion": {
                                                "type": "string"
                                            },
                                            "ExcepcionResidente": {"type": "string"},
                                            "ExcepcionNacimiento": {"type": "string"},
                                            "ExcepcionDomicilio": {"type": "string"},
                                            "ExcepcionTelefono": {"type": "string"},
                                            "ExcepcionOrdenPermanente": {
                                                "type": "string"
                                            },
                                            "ExcepcionFirma": {"type": "string"},
                                            "ParticipacionSociedadesUSA": {
                                                "type": "string"
                                            },
                                            "OrdenPermanente": {"type": "string"},
                                            "PaisResidencia": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "IdPersona": {
                                                            "type": "integer"
                                                        },
                                                        "IdPais": {"type": "integer"},
                                                        "Pais": {"type": "string"},
                                                        "Tin": {"type": "string"},
                                                        "NoTin": {"type": "string"},
                                                        "OtraCausa": {"type": "string"},
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                                "Portafolio": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "IdPortafolio": {"type": "integer"},
                                            "NombrePortafolio": {"type": "string"},
                                            "ValorPortafolio": {"type": "string"},
                                            "PorcentajeParticipacion": {
                                                "type": "string"
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            }
        }
    )(func)


from drf_spectacular.utils import extend_schema


def consultar_comprobante_facturacion_schema(func):
    return extend_schema(
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
                    "ResultadoComprobante": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "IdComprobante": {"type": "integer"},
                                "FolioComprobante": {"type": "integer"},
                                "FechaComprobante": {
                                    "type": "string",
                                    "format": "date",
                                },
                                "FechaLiquidacion": {
                                    "type": "string",
                                    "format": "date",
                                },
                                "NombreCliente": {"type": "string"},
                                "NombreEjecutivo": {"type": "string"},
                                "IdCondicionLiquidacion": {"type": "string"},
                                "IdTipoComprobante": {"type": "string"},
                                "IdTipoProducto": {"type": "string"},
                                "IdConcepto": {"type": "string"},
                                "Glosa": {"type": "string"},
                                "IdPortafolio": {"type": "string"},
                                "CodigoPortafolio": {"type": "string"},
                                "IdSucursalEmpleadoEjecutivoPortafolio": {
                                    "type": "integer"
                                },
                                "IdTipoOperacion": {"type": "string"},
                                "Monto": {"type": "number", "format": "float"},
                                "MontoComprobante": {
                                    "type": "number",
                                    "format": "float",
                                },
                                "MontoLiquidacionCobro": {
                                    "type": "number",
                                    "format": "float",
                                },
                                "MontoFinal": {"type": "number", "format": "float"},
                                "MontoPagado": {"type": "number", "format": "float"},
                                "MontoLiquidacion": {
                                    "type": "number",
                                    "format": "float",
                                },
                                "MontoComprobanteFinal": {
                                    "type": "number",
                                    "format": "float",
                                },
                                "IdEstadoComprobante": {"type": "string"},
                                "IdEstadoDTE": {"type": "string"},
                                "IdEstadoSII": {"type": "string"},
                                "Detalles": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "IdComprobante": {"type": "integer"},
                                            "NemotecnicoInstrumento": {
                                                "type": "string"
                                            },
                                            "Cantidad": {"type": "integer"},
                                            "Precio": {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            "Tasa": {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            "Monto": {
                                                "type": "number",
                                                "format": "float",
                                            },
                                            "IdFormaCustodia": {"type": "string"},
                                            "IdTipoProducto": {"type": "string"},
                                            "IdTipoInstrumento": {"type": "string"},
                                            "Descripcion": {"type": "string"},
                                            "FechaLiquidacion": {
                                                "type": "string",
                                                "format": "date",
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            }
        },
    )(func)
