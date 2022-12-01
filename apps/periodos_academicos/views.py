from django.views.generic import ListView

from apps.periodos_academicos.models import PeriodoAcademicoCursoPrograma

class ListadoPeriodoAcademicoCursoPrograma(ListView):
    model = PeriodoAcademicoCursoPrograma
    template_name = "periodos_academicos/periodos_cursos/listado.html"
    context_object_name = "periodos_cursos"
    queryset = PeriodoAcademicoCursoPrograma.obtener_por_periodo_academico_actual()


