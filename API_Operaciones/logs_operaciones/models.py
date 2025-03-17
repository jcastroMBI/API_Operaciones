from django.db import models


class OperacionesAPIRequestLog(models.Model):
    added_on = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación
    api = models.CharField(max_length=255)  # Endpoint de la API
    headers = models.JSONField()  # Cabeceras de la solicitud (Django 3.1+)
    body = models.TextField()  # Cuerpo de la solicitud
    method = models.CharField(max_length=10)  # Método HTTP
    client_ip_address = models.GenericIPAddressField()  # Dirección IP del cliente
    response = models.TextField()  # Respuesta de la API
    status_code = models.IntegerField()  # Código de estado de la respuesta
    execution_time = models.FloatField()  # Tiempo de ejecución en segundos
    source_url = models.CharField(
        max_length=255, blank=True, null=True
    )  # URL de origen de la solicitud

    class Meta:
        db_table = "operaciones_api_log"
