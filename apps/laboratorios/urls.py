from django.urls import path

from apps.laboratorios.views import (
    ListadoLaboratorios,
    RegistroLaboratorio,
    RegistroMasivoLaboratorios,
    ActualizarLaboratorio,

    ListadoPracticasLaboratorios,
    RegistroPracticasLaboratorio,
    ActualizarPracticasLaboratorio
)

app_name = 'laboratorios'


urlpatterns = [
    path("listado", ListadoLaboratorios.as_view(), name="listado"),
    path("registro", RegistroLaboratorio.as_view(), name="registro"),
    path("registro/masivo", RegistroMasivoLaboratorios.as_view(), name="registro_masivo"),
    path("actualizar/<int:id_laboratorio>", ActualizarLaboratorio.as_view(), name="actualizar"),

    path("practicas/listado", ListadoPracticasLaboratorios.as_view(), name="listado_practicas"),
    path("practicas/registro", RegistroPracticasLaboratorio.as_view(), name="registro_practica"),
    path("practicas/actualizar/<int:id_practica_laboratorio>", ActualizarPracticasLaboratorio.as_view(), name="actualizar_practica"),
]