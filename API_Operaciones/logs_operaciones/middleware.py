import re
from .models import OperacionesAPIRequestLog
import time
from django.http import JsonResponse


class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # Captura los datos de la solicitud
        method = request.method
        api = request.path
        headers = dict(request.headers)
        body = request.body.decode("utf-8")
        client_ip_address = request.META.get("REMOTE_ADDR")
        source_url = request.META.get(
            "HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR")
        )

        # Procesar la respuesta
        response = self.get_response(request)

        # Calcular el tiempo de ejecución
        execution_time = time.time() - start_time
        status_code = response.status_code
        response_body = response.content.decode("utf-8")

        filtered_body = re.sub(r"password=[^&]+", "password=****", body)

        filtered_response = re.sub(
            r'"refresh":"[^"]+"', '"refresh":"****"', response_body
        )
        filtered_response = re.sub(
            r'"access":"[^"]+"', '"access":"****"', filtered_response
        )

        if "Authorization" in headers:
            headers["Authorization"] = re.sub(
                r"Bearer [^ ]+", "Bearer ****", headers["Authorization"]
            )

        # Crear el log en la base de datos
        OperacionesAPIRequestLog.objects.create(
            added_on=response.headers.get("Date", None),
            api=api,
            headers=headers,
            body=filtered_body,
            method=method,
            client_ip_address=client_ip_address,
            response=filtered_response,
            status_code=status_code,
            execution_time=execution_time,
            source_url=source_url,
        )

        return response
