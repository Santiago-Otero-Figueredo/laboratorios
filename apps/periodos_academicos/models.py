from django.db import models
from django.db.models import QuerySet

from typing import List, Set
from apps.core.models import ModeloBase

class PeriodoAcademicoCursoPrograma(ModeloBase):
    curso_programa = models.ForeignKey(
        'cursos.CursoDelPrograma',
        verbose_name="Curso del programa",
        related_name="profesor_curso_programa_asociados",
        on_delete=models.PROTECT
    )
    periodo_academico = models.ForeignKey(
        'periodos_academicos.PeriodoAcademico',
        verbose_name="Periodo académico",
        related_name="profesor_curso_programa_asociados",
        on_delete=models.PROTECT
    )

    def __str__(self) -> str:
        return f'{self.curso_programa} - {self.periodo_academico}'

    def obtener_por_periodo_academico(periodo_academico_id: int) -> 'QuerySet[PeriodoAcademicoCursoPrograma]':
        return PeriodoAcademicoCursoPrograma.objects.filter(periodo_academico__pk=periodo_academico_id)

    def obtener_por_periodo_academico_actual() -> 'QuerySet[PeriodoAcademicoCursoPrograma]':
        return PeriodoAcademicoCursoPrograma.objects.filter(periodo_academico__pk=PeriodoAcademico.obtener_activo().pk)


class PeriodoAcademico(ModeloBase):
    PERIODO_UNO = "I"
    PERIODO_DOS = "II"
    PERIODO_TRES = "III"
    PERIODOS = (
        (PERIODO_UNO, "I"),
        (PERIODO_DOS, "II"),
        (PERIODO_TRES, "III"),
    )
    ano = models.PositiveIntegerField(verbose_name="año del periodo académico")
    periodo = models.CharField(max_length=3, choices=PERIODOS, verbose_name="periodo académico")
    cursos_del_programa = models.ManyToManyField(
        'cursos.CursoDelPrograma',
        related_name='periodos_acedemicos',
        verbose_name='Cursos del programa',
        through=PeriodoAcademicoCursoPrograma
    )
    fecha_inicio = models.DateField(verbose_name="fecha de inicio del periodo académico")
    fecha_fin = models.DateField(verbose_name="fecha de finalización del periodo académico")


    class Meta:
        ordering = ["-ano", "-periodo"]
        unique_together = (("ano", "periodo",),)
        permissions = (
            ("gestionar_periodos_academicos", "Periodos académicos - Gestionar"),
        )

    def __str__(self):
        return "{}-{}".format(self.ano, self.periodo)

    @staticmethod
    def obtener_activo():
        try:
            return PeriodoAcademico.objects.get(activa=True)
        except PeriodoAcademico.DoesNotExist:
            return None

    @staticmethod
    def obtener_periodos_academicos_por_ano(ano: int) -> QuerySet['PeriodoAcademico']:
        return PeriodoAcademico.obtener_activos().filter(ano=ano).order_by('periodo')

    @staticmethod
    def obtener_periodos_academicos_por_ano_y_lista_ids(ano: int, lista_ids: List[int]) -> QuerySet['PeriodoAcademico']:
        return PeriodoAcademico.obtener_por_lista_ids(lista_ids).filter(ano=ano).order_by('periodo')

    @staticmethod
    def obtener_anos() -> Set[int]:
        return set(PeriodoAcademico.obtener_activos().values_list('ano', flat=True))


