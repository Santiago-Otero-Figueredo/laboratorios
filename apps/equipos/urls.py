from django.urls import path

from apps.equipos.views import (
    ListadoEquipos,
    RegistroEquipo,
    ActualizarEquipo,

    ListadoTipoEquipos,
    RegistroTipoEquipo,
    ActualizarTipoEquipo,

    ListadoCamposExtra,
    RegistroCampoExtra,
    ActualizarCampoExtra,

    ListadoInformacionAdicionalEquipos,
    RegistroInformacionAdicionalEquipo,
    ActualizarInformacionAdicionalEquipo
)

app_name = 'equipos'


urlpatterns = [
    path("listado", ListadoEquipos.as_view(), name="listado"),
    path("registro", RegistroEquipo.as_view(), name="registro"),
    path("actualizar/<int:id_equipo>", ActualizarEquipo.as_view(), name="actualizar"),

    path("tipos/listado", ListadoTipoEquipos.as_view(), name="listado_tipos"),
    path("tipos/registro", RegistroTipoEquipo.as_view(), name="registro_tipo"),
    path("tipos/actualizar/<int:id_tipo_equipo>", ActualizarTipoEquipo.as_view(), name="actualizar_tipo"),

    path("campos/listado", ListadoCamposExtra.as_view(), name="listado_campos"),
    path("campos/registro", RegistroCampoExtra.as_view(), name="registro_campo"),
    path("campos/actualizar/<int:id_campo_extra>", ActualizarCampoExtra.as_view(), name="actualizar_campo"),

    path("informacion-adicional/<int:id_equipo>/listado", ListadoInformacionAdicionalEquipos.as_view(), name="listado_informacion"),
    path("informacion-adicional/<int:id_equipo>/registro", RegistroInformacionAdicionalEquipo.as_view(), name="registro_informacion"),
    path("informacion-adicional/actualizar/<int:id_informacion_adicional>", ActualizarInformacionAdicionalEquipo.as_view(), name="actualizar_informacion"),

]