import re


def swagger_preprocessing_hook(endpoints):
    # Paths restringidos
    restricted_paths = [
        r"^/Operaciones/Plataforma/consultarPrecioInstrumentos/{nombre_instrumento}/$",
    ]

    # Ocultamos los paths restringidos si el usuario no es superuser
    filtered_endpoints = []
    for path, path_regex, method, callback in endpoints:
        # Verifica si la ruta coincide completamente con los patrones restringidos
        if not any(re.fullmatch(pattern, path) for pattern in restricted_paths):
            filtered_endpoints.append((path, path_regex, method, callback))

    return filtered_endpoints
