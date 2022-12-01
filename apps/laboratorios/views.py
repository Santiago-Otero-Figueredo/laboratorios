from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from apps.laboratorios.models import Laboratorio, PracticaLaboratorio
from apps.laboratorios.forms import FormLaboratorio, FormPracticaLaboratorio

class ListadoLaboratorios(ListView):
    model = Laboratorio
    template_name = "laboratorios/listado.html"
    context_object_name = "laboratorios"


class RegistroLaboratorio(CreateView):
    model = Laboratorio
    template_name = "laboratorios/registro.html"
    form_class = FormLaboratorio
    success_url = reverse_lazy('laboratorios:listado')


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


class ActualizarPracticasLaboratorio(UpdateView):
    model = PracticaLaboratorio
    template_name = "laboratorios/practicas/registro.html"
    form_class = FormPracticaLaboratorio
    success_url = reverse_lazy('laboratorios:listado_practicas')
    pk_url_kwarg = "id_practica_laboratorio"