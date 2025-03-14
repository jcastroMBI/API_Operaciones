import os
from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url=os.getenv("SELF_URL") + "/schema/"),
        name="swagger-ui",
    ),
]
