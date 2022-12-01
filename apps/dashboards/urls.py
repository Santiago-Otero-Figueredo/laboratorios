from django.urls import path

from apps.dashboards.views import Inicio

app_name = "dashboards"
urlpatterns = [
    path("inicio/", Inicio.as_view(), name='inicio')
]