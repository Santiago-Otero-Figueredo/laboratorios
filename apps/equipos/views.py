from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View, FormView

from apps.equipos.models import Equipo, TipoEquipo, CampoExtra, InformacionAdicionalEquipo
from apps.equipos.forms import FormEquipo, FormTipoEquipo, FormCampoExtra, FormInformacionAdicionalEquipo

from apps.core.classes import LecturaExcelPandas
from apps.core.forms import FormRegistroMasivo


class ListadoEquipos(ListView):
    model = Equipo
    template_name = "equipos/listado.html"
    context_object_name = "equipos"


class RegistroEquipo(CreateView):
    model = Equipo
    template_name = "equipos/registro.html"
    form_class = FormEquipo
    success_url = reverse_lazy('equipos:listado')


class ActualizarEquipo(UpdateView):
    model = Equipo
    template_name = "equipos/registro.html"
    form_class = FormEquipo
    success_url = reverse_lazy('equipos:listado')
    pk_url_kwarg = "id_equipo"

## TipoEquipo

class ListadoTipoEquipos(ListView):
    model = TipoEquipo
    template_name = "equipos/tipo_equipos/listado.html"
    context_object_name = "tipo_equipos"


class RegistroTipoEquipo(CreateView):
    model = TipoEquipo
    template_name = "equipos/tipo_equipos/registro.html"
    form_class = FormTipoEquipo
    success_url = reverse_lazy('equipos:listado_tipos')

class RegistroMasivoTiposEquipos(FormView):
    template_name = "equipos/tipo_equipos/registro_masivo.html"
    form_class = FormRegistroMasivo
    success_url = reverse_lazy('equipos:listado_tipos')

    def form_valid(self, form):
        archivo = form.cleaned_data['archivo']
        gestor_archivo = LecturaExcelPandas(
            archivo=archivo,
            columnas_esperadas=['NOMBRE_EQUIPO', 'MARCA', 'MODELO', 'SERIE', 'CAPACIDAD',
                'AMPERAJE', 'PRESION', 'VOLTAJE', 'FABRICANTE', 'FRECUENCIA', 'VELOCIDAD','POTENCIA',
                'RANGO_1', 'RANGO_2', 'RANGO_3', 'UND_DE_MEDIDA_1', 'UND_DE_MEDIDA_2', 'UND_DE_MEDIDA_3',
                'EXACTITUD_1', 'EXACTITUD_2', 'EXACTITUD_3', 'RESOLUCION_1', 'RESOLUCION_2', 'RESOLUCION_3'],
            prohibir_celdas_vacias=False,
            modelo=TipoEquipo,
            columnas_a_normalizar=['NOMBRE_EQUIPO'],
            columnas_ignorar=['No_INVENTARIO', 'ACCESORIOS', 'CODIGO_ACCESORIOS',
                'UBICACION', 'FECHA_ULTIMO_PROXIMO_MANTENIMIENTO', 'FECHA_ULTIMA_Y_PROXIMA_CALIBRACION']
        )

        respuesta = gestor_archivo._obtener_datos_cargados()
        if respuesta['resultado'] is False:
            messages.error(self.request, f'Fallo al cargar los datos {respuesta["errores"]}')
            return super().form_invalid(form)

        TipoEquipo.registro_masivo(respuesta['datos'])
        messages.success(self.request, 'Tipos de equipos cargados con éxito')
        return super().form_valid(form)



class ActualizarTipoEquipo(UpdateView):
    model = TipoEquipo
    template_name = "equipos/tipo_equipos/registro.html"
    form_class = FormTipoEquipo
    success_url = reverse_lazy('equipos:listado_tipos')
    pk_url_kwarg = "id_tipo_equipo"


## CampoExtra

class ListadoCamposExtra(ListView):
    model = CampoExtra
    template_name = "equipos/campos_extra/listado.html"
    context_object_name = "campos_extra"


class RegistroCampoExtra(CreateView):
    model = CampoExtra
    template_name = "equipos/campos_extra/registro.html"
    form_class = FormCampoExtra
    success_url = reverse_lazy('equipos:listado_campos')

class ActualizarCampoExtra(UpdateView):
    model = CampoExtra
    template_name = "equipos/campos_extra/registro.html"
    form_class = FormCampoExtra
    success_url = reverse_lazy('equipos:listado_campos')
    pk_url_kwarg = "id_campo_extra"

#InformacionAdicionalEquipo

class VistaGeneralOperacionesEquipos(View):

    def dispatch(self, request, *args, **kwargs):
        id_equipo = self.kwargs.pop('id_equipo', -1)
        self.equipo = Equipo.obtener_por_id(id_equipo)
        if self.equipo is None:
            messages.error(request, "El equipo al que desea acceder NO existe")
            return redirect('equipos:listado')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipo'] = self.equipo
        return context

class ListadoInformacionAdicionalEquipos(VistaGeneralOperacionesEquipos, ListView):
    model = InformacionAdicionalEquipo
    template_name = "equipos/informacion_adicional/listado.html"
    context_object_name = "informacion_adicional"

    def get_queryset(self):
        return self.equipo.obtener_detalles_informacion_adicional()


class RegistroInformacionAdicionalEquipo(VistaGeneralOperacionesEquipos, CreateView):
    model = InformacionAdicionalEquipo
    template_name = "equipos/informacion_adicional/registro.html"
    form_class = FormInformacionAdicionalEquipo

    def get_initial(self):
        initial = super().get_initial()
        initial['equipo'] = self.equipo
        return initial

    def get_success_url(self) -> str:
        return reverse_lazy('equipos:listado_informacion', kwargs={'id_equipo':self.equipo.pk})



class ActualizarInformacionAdicionalEquipo(UpdateView):
    model = InformacionAdicionalEquipo
    template_name = "equipos/informacion_adicional/registro.html"
    form_class = FormInformacionAdicionalEquipo
    pk_url_kwarg = "id_informacion_adicional"

    def dispatch(self, request, *args, **kwargs):
        self.equipo = self.get_object().equipo
        self.campo_extra_tipo = self.get_object().campo_extra_tipo
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipo'] = self.equipo
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['equipo'] = self.equipo
        initial['campo_extra_tipo'] = self.campo_extra_tipo
        return initial

    def get_success_url(self) -> str:
        return reverse_lazy('equipos:listado_informacion', kwargs={'id_equipo':self.equipo.pk})

