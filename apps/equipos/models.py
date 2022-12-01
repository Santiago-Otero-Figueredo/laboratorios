from django.db import models
from django.db.models import QuerySet
from django.core.validators import MinValueValidator

from apps.core.models import ModeloBase
# Create your models here.

class TipoEquipo(ModeloBase):
    campos_extra = models.ManyToManyField(
        'equipos.CampoExtra',
        related_name="tipo_equipos_asociados",
        verbose_name="Campos extra asociado",
        through="equipos.CampoExtraTipoEquipo",
        blank=False
    )
    nombre = models.CharField(max_length=255, verbose_name="Nombre", unique=True)

    def __str__(self) -> str:
        return f'{self.nombre}'

class Equipo(ModeloBase):
    tipo_equipo = models.ForeignKey(
        TipoEquipo,
        related_name="equipos_asociados",
        verbose_name="Tipo equipo asociado",
        on_delete=models.PROTECT,
    )
    laboratorio = models.ForeignKey(
        'laboratorios.Laboratorio',
        related_name="equipos_asociados",
        verbose_name="Laboratorio asociado",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    accesorios = models.ManyToManyField(
        'equipos.Accesorio',
        related_name='equipos_asociados',
        verbose_name="Accesorios del equipo",
        through='equipos.AccesorioEquipo'
    )
    informacion_adicional = models.ManyToManyField(
        'equipos.CampoExtraTipoEquipo',
        related_name='equipos_asociados',
        verbose_name="Información adicional del equipo",
        through='equipos.InformacionAdicionalEquipo'
    )
    serial = models.CharField(max_length=60, verbose_name="Numero serial del equipo", unique=True)

    def __str__(self) -> str:
        return f'{self.serial}'

    def obtener_compras_realizadas(self) -> 'QuerySet[CompraEquipo]':
        return self.compras_realizadas.all()

    def obtener_detalles_informacion_adicional(self) -> 'QuerySet[InformacionAdicionalEquipo]':
        """
            Obtiene la información detallada de cada relación que hay entre la instancia de equipo y
            el modelo CampoExtraTipoEquipo, esa información es el campo valor del modelo InformacionAdicionalEquipo
        """
        return self.informacion_adicional_equipo_asociados.all()


class CompraEquipo(ModeloBase):
    equipo = models.ForeignKey(
        Equipo,
        related_name="compras_realizadas",
        verbose_name="Equipos comprados",
        on_delete=models.PROTECT
    )
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad de equipos comprados", validators=[MinValueValidator(1)])
    fecha = models.DateField()
    descripcion = models.TextField(verbose_name="Descripción compra", default="", blank=True)
    valor = models.FloatField(verbose_name="Valor total de la compra", validators=[MinValueValidator(0.0)])

    def __str__(self) -> str:
        return f'{self.equipo} - {self.cantidad}'


class Accesorio(ModeloBase):
    nombre = models.CharField(max_length=255, verbose_name="Nombre del tipo equipo", unique=True)

    def __str__(self) -> str:
        return f'{self.nombre}'


class AccesorioEquipo(ModeloBase):
    equipo = models.ForeignKey(
        Equipo,
        related_name="accesorio_equipos_asociados",
        verbose_name="Equipo asociado",
        on_delete=models.PROTECT
    )
    accesorio = models.ForeignKey(
        Accesorio,
        related_name="accesorio_equipos_asociados",
        verbose_name="Accesorio asociado",
        on_delete=models.PROTECT
    )
    codigo = models.CharField(max_length=60, verbose_name="Código del accesorio asociado al equipo")

    def __str__(self) -> str:
        return f'{self.equipo} - {self.accesorio} - {self.codigo}'


class CampoExtra(ModeloBase):
    nombre = models.CharField(max_length=60, verbose_name="Campo extra con información adicional", unique=True)

    def __str__(self) -> str:
        return f'{self.nombre}'


class CampoExtraTipoEquipo(ModeloBase):
    tipo_equipo = models.ForeignKey(
        TipoEquipo,
        related_name="campo_extra_tipo_equipo_asociados",
        verbose_name="Tipo equipo asociado",
        on_delete=models.PROTECT
    )
    campo_extra = models.ForeignKey(
        CampoExtra,
        related_name="campo_extra_tipo_equipo_asociados",
        verbose_name="campo extra asociado",
        on_delete=models.PROTECT
    )

    def __str__(self) -> str:
        return f'{self.tipo_equipo} - {self.campo_extra}'

    @staticmethod
    def obtener_por_tipo_equipo(id_tipo_equipo: int) -> 'QuerySet[CampoExtraTipoEquipo]':
        return CampoExtraTipoEquipo.obtener_activos().filter(tipo_equipo__pk=id_tipo_equipo)


class InformacionAdicionalEquipo(ModeloBase):
    equipo = models.ForeignKey(
        Equipo,
        related_name="informacion_adicional_equipo_asociados",
        verbose_name="Equipo asociado",
        on_delete=models.PROTECT
    )
    campo_extra_tipo = models.ForeignKey(
        CampoExtraTipoEquipo,
        related_name="informacion_adicional_equipo_asociados",
        verbose_name="Campo extra del tipo asociado",
        on_delete=models.PROTECT
    )
    valor = models.CharField(max_length=255, verbose_name="Información adicional entre el tipo de equipo y el campo asociado")

    def __str__(self) -> str:
        return f'{self.equipo} - {self.campo_extra_tipo} - {self.valor}'