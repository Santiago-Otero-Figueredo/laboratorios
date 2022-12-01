from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, FormView

from apps.core.classes import LecturaExcelPandas

from apps.laboratorios.models import Laboratorio, PracticaLaboratorio

from apps.laboratorios.forms import FormLaboratorio, FormPracticaLaboratorio
from apps.core.forms import FormRegistroMasivo

class ListadoLaboratorios(ListView):
    model = Laboratorio
    template_name = "laboratorios/listado.html"
    context_object_name = "laboratorios"


class RegistroLaboratorio(CreateView):
    model = Laboratorio
    template_name = "laboratorios/registro.html"
    form_class = FormLaboratorio
    success_url = reverse_lazy('laboratorios:listado')


class RegistroMasivoLaboratorios(FormView):
    template_name = "laboratorios/registro_masivo.html"
    form_class = FormRegistroMasivo
    success_url = reverse_lazy('laboratorios:listado')

    def form_valid(self, form):
        archivo = form.cleaned_data['archivo']
        print("############ ARCHIVO CARGADO ###########")
        gestor_archivo = LecturaExcelPandas(
            archivo=archivo,
            columnas_esperadas=['LABORATORIO'],
            prohibir_celdas_vacias=True
        )

        resultado, datos, errores = gestor_archivo._obtener_datos_cargados()
        if resultado is False:
            messages.error(self.request, f'Fallo al cargar los datos {errores}')
            return super().form_invalid(form)

        Laboratorio.registro_masivo(datos)
        messages.success(self.request, 'Laboratorios cargados con éxito')
        return super().form_valid(form)



class ActualizarLaboratorio(UpdateView):
    model = Laboratorio
    template_name = "laboratorios/registro.html"
    form_class = FormLaboratorio
    success_url = reverse_lazy('laboratorios:listado')
    pk_url_kwarg = "id_laboratorio"


#Practicas
class ListadoPracticasLaboratorios(ListView):
    model = PracticaLaboratorio
    template_name = "laboratorios/practicas/listado.html"
    context_object_name = "practicas_laboratorio"


class RegistroPracticasLaboratorio(CreateView):
    model = PracticaLaboratorio
    template_name = "laboratorios/practicas/registro.html"
    form_class = FormPracticaLaboratorio
    success_url = reverse_lazy('laboratorios:listado_practicas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.core.utils import construir_dict_calendario_timeline
        practicas_registradas = list(PracticaLaboratorio.agendadas_por_laboratorio(1).values("nombre", "fecha_inicio", "fecha_fin"))


        practicas_registradas = construir_dict_calendario_timeline(practicas_registradas, {'nombre':'title', 'fecha_inicio':'start', 'fecha_fin':'end'})



        context['practicas_registradas'] = practicas_registradas
        return context


class ActualizarPracticasLaboratorio(UpdateView):
    model = PracticaLaboratorio
    template_name = "laboratorios/practicas/registro.html"
    form_class = FormPracticaLaboratorio
    success_url = reverse_lazy('laboratorios:listado_practicas')
    pk_url_kwarg = "id_practica_laboratorio"