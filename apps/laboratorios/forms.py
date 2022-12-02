from django import forms

from apps.core.forms import ModelSelect2WidgetConfigurable
from apps.laboratorios.models import Laboratorio, PracticaLaboratorio
from apps.periodos_academicos.models import PeriodoAcademicoCursoPrograma

class FormLaboratorio(forms.ModelForm):

    class Meta:
        model = Laboratorio
        fields = ('nombre', 'descripcion', 'activa')


class FormPracticaLaboratorio(forms.ModelForm):

    laboratorio = ModelSelect2WidgetConfigurable(
        model = Laboratorio,
        queryset = Laboratorio.obtener_activos(),
        search_fields = ['nombre__icontains'],
        label='Laboratorio'
    )

    grupo = ModelSelect2WidgetConfigurable(
        model = PeriodoAcademicoCursoPrograma,
        queryset = PeriodoAcademicoCursoPrograma.obtener_por_periodo_academico_actual(),
        search_fields = [
            'curso_programa__nombre__icontains',
            'curso_programa__codigo__icontains',
            'cursos_del_programa__curso__nombre__icontains',
            'cursos_del_programa__programa__nombre__icontains'
        ],
        label='Grupo'
    )


    class Meta:
        model = PracticaLaboratorio
        fields = ('nombre', 'laboratorio', 'grupo', 'fecha_inicio', 'fecha_fin', 'activa')


    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self.fields['fecha_inicio'].widget.attrs['class'] = 'fecha_acordada'
        self.fields['fecha_fin'].widget.attrs['class'] = 'fecha_acordada'

    def clean(self):
        cleaned_data = super().clean()
        laboratorio = cleaned_data.get("laboratorio")
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        practicas_agendadas = PracticaLaboratorio.agendadas_por_laboratorio_en_rango__fechas(laboratorio.pk, fecha_inicio, fecha_fin)
        if practicas_agendadas.exists():
            mensaje = f'Ya hay {len(practicas_agendadas)} practica(s) agendada para ese rango de fechas'
            self.add_error('fecha_inicio', mensaje)
            self.add_error('fecha_fin', mensaje)

        if fecha_inicio > fecha_fin:
            mensaje = f'La fecha final no puede ser antes que la inicial'
            self.add_error('fecha_fin', mensaje)

        return super().clean()