# myapp/hooks.py
import re


def swagger_preprocessing_hook(endpoints):
    # Paths restringidos
    restricted_paths = [
        r"^/optimus/instrumento/{nombre_instrumento}/$",
    ]

    # Ocultamos los paths restringidos si el usuario no es superuser
    filtered_endpoints = []
    for path, path_regex, method, callback in endpoints:
        if not any(re.match(pattern, path) for pattern in restricted_paths):
            filtered_endpoints.append((path, path_regex, method, callback))

    return filtered_endpoints
