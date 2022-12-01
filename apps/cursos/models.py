from django.db import models
from django.db.models import QuerySet

from typing import TYPE_CHECKING, List

from apps.core.models import ModeloBase
from apps.programas.models import Programa


class Curso(ModeloBase):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del curso")
    codigo = models.CharField(max_length=10, verbose_name="Código del curso")
    programas = models.ManyToManyField(Programa, through='CursoDelPrograma')

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


    @staticmethod
    def obtener_cursos_por_estudiante_y_periodo_academico(
        id_estudiante: int,
        id_periodo_academico: int
    ) -> QuerySet['Curso']:

        return Curso.objects.filter(
            programas_del_curso__matriculas_del_cursoprograma__estudiante = id_estudiante,
            programas_del_curso__matriculas_del_cursoprograma__periodo_academico = id_periodo_academico
        )

    @staticmethod
    def obtener_cursos_por_profesor_periodo_academico_y_programa(
        id_profesor: int,
        id_periodo_academico: int,
        id_programa: int,
    ) -> QuerySet['Curso']:

        return Curso.objects.filter(
            programas__pk=id_programa,
            programas_del_curso__profesor_curso_programa_asociados__profesor = id_profesor,
            programas_del_curso__profesor_curso_programa_asociados__periodo_academico__pk=id_periodo_academico
        )



class CursoDelPrograma(ModeloBase):
    curso = models.ForeignKey(Curso, related_name="programas_del_curso", on_delete=models.PROTECT)
    programa = models.ForeignKey(Programa, related_name="cursos_del_programa", on_delete=models.PROTECT)
    prerrequisito = models.ForeignKey("self", related_name="siguientes_cursos_del_programa", null=True, on_delete=models.PROTECT)


    class Meta:
        ordering = ("programa", "curso",)

    def __str__(self):
        return f"{self.programa} - {self.curso}"

    def obtener_por_curso_programa_id(id_curso, id_programa):
        try:
            return CursoDelPrograma.objects.get(
                curso__id=id_curso,
                programa__id=id_programa
            )
        except:
            return None





