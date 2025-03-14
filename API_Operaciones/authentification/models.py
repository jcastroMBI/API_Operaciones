from django.db import models
from django.contrib.auth.models import AbstractUser


class AgenteUser(AbstractUser):
    codigoagente = models.CharField(max_length=7, null=True, blank=True)
    rut_agente = models.CharField(max_length=12, null=True, blank=True)
    ruteador = models.BooleanField(default=False)

    groups = None
    user_permissions = None
