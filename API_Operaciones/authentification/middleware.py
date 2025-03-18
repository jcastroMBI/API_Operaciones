import os
import re
from django.http import JsonResponse


class RestrictOriginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_paths = [
            r"^/Operaciones/Plataforma/consultarPrecioInstrumentos/\d+/$",
        ]

        # Obtener el origen de la solicitud
        origin = request.headers.get("Origin")

        # Bloquear todas las peticiones desde DOCS excepto /schema/
        if origin == os.getenv("DOCS_URL") and not request.path.startswith("/schema/"):
            return JsonResponse(
                {"detail": "Access denied for this origin."}, status=403
            )

        # Validar si la ruta actual coincide con alguno de los patrones
        for pattern in restricted_paths:
            if re.match(pattern, request.path):
                if origin != os.getenv("FRONTEND_URL"):
                    return JsonResponse(
                        {"detail": "Access denied from this origin."}, status=403
                    )

        response = self.get_response(request)
        return response
