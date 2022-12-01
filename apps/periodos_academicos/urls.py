from django.urls import path

from apps.periodos_academicos .views import (
    ListadoPeriodoAcademicoCursoPrograma,
)

app_name = 'periodos_academicos'


urlpatterns = [
    path("cursos-programa/listado", ListadoPeriodoAcademicoCursoPrograma.as_view(), name="listado_cursos_programa"),
]