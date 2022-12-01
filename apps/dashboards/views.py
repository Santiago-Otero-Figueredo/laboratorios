from django.views.generic import ListView, TemplateView, FormView

from apps.dashboards.models import Reporte
from apps.matriculas.models import Matricula
from apps.periodos_academicos.models import PeriodoAcademico
from apps.programas.models import Programa

from apps.dashboards.forms import FiltroPeriodoProgramaForm, FiltroNivelesEvaluacionPorProfesorForm, FiltroProgramaForm, FiltroCalificacionesPorActividadForm
from apps.usuarios.models import Usuario


class Inicio(TemplateView):
    template_name = "dashboard/inicio.html"