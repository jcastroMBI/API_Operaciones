from django.core.cache import cache
from django.utils import timezone
import os

maximo_llamadas_diarias = os.getenv("LLAMADAS_DIARIAS")


def llamadas_restantes(user_id):
    """
    Obtiene la cantidad de llamadas restantes del cache o crea una entrada nueva si no existe.

    Args:
        user_id (int): ID del usuario.

    Returns:
        int: Cantidad de llamadas restantes.
    """
    cache_key = f"api_calls_{user_id}"
    remaining_calls = cache.get(cache_key)

    if remaining_calls is None:
        reset_time = timezone.localtime().replace(
            hour=23, minute=59, second=59, microsecond=0
        )

        cache.set(
            cache_key,
            maximo_llamadas_diarias,
            (reset_time - timezone.localtime()).total_seconds(),
        )

        remaining_calls = maximo_llamadas_diarias

    return remaining_calls


def usar_llamadas(user_id, cantidad_llamadas):
    """
    Usa una cantidad de llamadas diarias del usuario.

    Args:
        user_id (int): ID del usuario.
        cantidad_llamadas (int): cantidad de llamadas que va a usar el usuario.

    Returns:
        None
    """
    cache_key = f"api_calls_{user_id}"
    cache.incr(cache_key, -cantidad_llamadas)
