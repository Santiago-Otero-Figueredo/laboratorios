from django.db import models
from django.db.models import QuerySet
from django.core.validators import MinValueValidator


from apps.core.models import ModeloBase
# Create your models here.

class Laboratorio(ModeloBase):
    nombre = models.CharField(max_length=60, verbose_name="Nombre del laboratorio")
    descripcion = models.TextField(verbose_name="Descripción", default="", blank=True)

    def __str__(self) -> str:
        return self.nombre

    def obtener_equipo(self, id_equipo: int) -> 'Laboratorio':
        try:
            return self.equipo_laboratorio_asignado.get(equipo__pk=id_equipo)
        except:
            return None

    def esta_asignado_equipo(self, id_equipo: int) -> bool:

        return self.equipo_laboratorio_asignado.filter(equipo__pk=id_equipo)




class PracticaLaboratorio(ModeloBase):
    laboratorio = models.ForeignKey(
        Laboratorio,
        related_name="practicas_laboratorios_asignados",
        verbose_name="Laboratorio asignado",
        on_delete=models.PROTECT
    )
    grupo = models.ForeignKey(
        "periodos_academicos.PeriodoAcademicoCursoPrograma",
        related_name='practicas_laboratorios_asignados',
        verbose_name="Grupo asignado",
        on_delete=models.PROTECT
    )
    alertas = models.ManyToManyField(
        'equipos.Equipo',
        related_name="practicas_laboratorios_asignadas",
        verbose_name="Alertas generadas",
        through="laboratorios.Alerta"
    )
    nombre = models.CharField(max_length=60, verbose_name="Nombre del laboratorio")
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()


    def __str__(self) -> str:
        return f'{self.laboratorio} - {self.grupo}'

    @staticmethod
    def agendadas_por_laboratorio_en_rango__fechas(id_laboratorio: int, fecha_inicio: 'datetime', fecha_fin:'datetime') -> 'QuerySet[PracticaLaboratorio]':

        return PracticaLaboratorio.objects.filter(
                laboratorio__pk=id_laboratorio,
                fecha_inicio__lt=fecha_fin,
                fecha_fin__gt=fecha_inicio
            )


class EquipoPracticaLaboratorio(ModeloBase):
    tipo_equipo = models.ForeignKey(
        'equipos.TipoEquipo',
        related_name="equipo_practica_asignado",
        verbose_name="Tipos equipo asignados a la practica",
        on_delete=models.PROTECT
    )
    practica_laboratorio = models.ForeignKey(
        PracticaLaboratorio,
        related_name="equipo_practica_asignado",
        verbose_name="Laboratorio asignado a la practica",
        on_delete=models.PROTECT
    )
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad de equipos asignados a la practica", validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return f'{self.equipo} - {self.practica_laboratorio} - {self.cantidad}'

class Alerta(ModeloBase):
    equipo = models.ForeignKey(
        'equipos.Equipo',
        related_name="alerta_generada",
        verbose_name="Equipos con alerta",
        on_delete=models.PROTECT
    )
    practica_laboratorio = models.ForeignKey(
        PracticaLaboratorio,
        related_name="alerta_generada",
        verbose_name="Practica de laboratorio con alerta",
        on_delete=models.PROTECT
    )
    nombre = models.CharField(max_length=60, verbose_name="Nombre de la alerta")
    descripcion = models.TextField(verbose_name="Descripción", default="", blank=True)

    def __str__(self) -> str:
        return f'{self.equipo} - {self.practica_laboratorio} - {self.nombre}'