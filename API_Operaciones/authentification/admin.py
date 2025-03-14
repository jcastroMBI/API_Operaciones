from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AgenteUser


@admin.register(AgenteUser)
class AgenteUserAdmin(UserAdmin):
    list_display = ("username", "email", "codigoagente", "is_active", "is_staff")
    ordering = ("email",)

    # Personalización de los campos para evitar errores
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Información personal",
            {"fields": ("email", "codigoagente", "rut_agente", "ruteador")},
        ),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "codigoagente",
                    "rut_agente",
                    "ruteador",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    # Remover grupos y permisos de las configuraciones
    filter_horizontal = ()
    list_filter = ("is_staff", "is_superuser", "is_active")
