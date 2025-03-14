from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("authentification.urls")),
    path("Operaciones/", include("operaciones.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Quitar en caso de querer separar los docs
    # path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
