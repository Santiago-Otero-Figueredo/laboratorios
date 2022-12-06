from django.db import models
from django.db.models import QuerySet
from django.core.validators import MinValueValidator, RegexValidator

from typing import Dict, Union, List, Optional

from apps.laboratorios.models import Laboratorio

from apps.core.models import ModeloBase
from apps.core.utils import normalizar_nombres

from django.db.models.signals import pre_save
from django.dispatch import receiver

import pandas as pd
# Create your models here.

class TipoEquipo(ModeloBase):

    REGISTRO_MASIVO_COLUMNAS_IGORAR = [
        'no_inventario', 'accesorios', 'codigo_accesorios', 'laboratorio',
        'ubicacion', 'fecha_ultimo_mantenimiento', 'fecha_proximo_mantenimiento',
        'fecha_ultima_calibracion', 'fecha_proxima_calibracion'
    ]

    campos_extra = models.ManyToManyField(
        'equipos.CampoExtra',
        related_name="tipo_equipos_asociados",
        verbose_name="Campos extra asociado",
        through="equipos.CampoExtraTipoEquipo",
        blank=False
    )
    nombre = models.TextField(verbose_name="Nombre", unique=True)
    descripcion = models.TextField(verbose_name="Descripción", default="")


    def __str__(self) -> str:
        return f'{self.nombre}'

    @staticmethod
    def obtener_nombres_cargue_masivo_data_frame(df_datos: pd.DataFrame):
        columnas_df_tipos = list(set(df_datos.columns) - set(TipoEquipo.REGISTRO_MASIVO_COLUMNAS_IGORAR))
        df_tipos_simplificado = pd.DataFrame(df_datos['nombre_equipo'], columns=columnas_df_tipos)
        return df_tipos_simplificado

    @staticmethod
    def existe_por_nombre(nombre: str) -> bool:
        return TipoEquipo.obtener_todos().filter(nombre__iexact=nombre).exists()

    @staticmethod
    def obtener_por_nombre(nombre: str) -> Optional['TipoEquipo']:
        try:
            return TipoEquipo.obtener_todos().get(nombre__iexact=nombre)
        except:
            return None

    @staticmethod
    def validar_registro_masivo(nombres_tipo_equipo: set, prohibir_duplicados: bool=False) -> Dict[str, Union[bool, str, List[str]]]:

        mensajes_error = []

        tipos_equipos_nuevos = set(map(normalizar_nombres, nombres_tipo_equipo)) # Eliminando caracteres \-\.\n\t

        respuesta = {'resultado':True, 'errores':[], 'datos':tipos_equipos_nuevos}

        tipos_equipos_actuales = set(TipoEquipo.obtener_todos().values_list('nombre', flat=True))

        if prohibir_duplicados and (tipos_equipos_nuevos & tipos_equipos_actuales):
            mensajes_error.append({'modelo':'Hay tipos de equipos ya registrados'})

        if len(mensajes_error) > 0:
            respuesta.update({'resultado':False, 'errores':mensajes_error})

        return respuesta

    @staticmethod
    def registro_masivo(df_tipos_equipo: pd.DataFrame, prohibir_duplicados: bool=False) -> Dict[str, Union[bool, str, List[str]]]:

        nombres_tipo_equipo = set(df_tipos_equipo.nombre_equipo.unique())
        respuesta = TipoEquipo.validar_registro_masivo(nombres_tipo_equipo, prohibir_duplicados)
        resultado = respuesta['resultado']
        datos = respuesta['datos']

        if resultado:
            campos_extra_relacionados = list(set(map(normalizar_nombres, df_tipos_equipo.columns)))
            campos_extra_relacionados.remove('nombre_equipo')
            CampoExtra.registro_masivo(campos_extra_relacionados)
            campos_asociar = CampoExtra.obtener_por_listado_nombres(campos_extra_relacionados)
            for tipo_equipo in datos:
                if tipo_equipo: # Si no es un caracter vacio
                    print(tipo_equipo, " : ", TipoEquipo.existe_por_nombre(tipo_equipo.strip()))
                    if not TipoEquipo.existe_por_nombre(tipo_equipo.strip()):
                        tipo_equipo = TipoEquipo.objects.create(nombre=tipo_equipo.strip())
                    else:
                        tipo_equipo = TipoEquipo.obtener_por_nombre(nombre=tipo_equipo.strip())
                    tipo_equipo.campos_extra.add(*campos_asociar)
                    tipo_equipo.save()

        return respuesta


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

    @staticmethod
    def validar_registro_masivo(df_equipos: pd.DataFrame,
        prohibir_duplicados_equipos:bool=False,
        prohibir_duplicados_tipos: bool=False,
        prohibir_duplicados_laboratorios: bool=False) -> Dict[str, Union[bool, str, List[str]]]:

        mensajes_error = []

        equipos_nuevos = set(df_equipos.no_inventario.unique())
        equipos_nuevos = set(map(normalizar_nombres, equipos_nuevos)) # Eliminando caracteres \-\.\n\t

        respuesta = {'resultado':True, 'errores':[], 'datos':df_equipos}

        equipos_actuales = set(TipoEquipo.obtener_todos().values_list('nombre', flat=True))

        df_tipos = df_equipos.copy()
        df_tipos_simplificado = TipoEquipo.obtener_nombres_cargue_masivo_data_frame(df_tipos)
        nombres_tipo_equipo = set(df_tipos_simplificado.nombre_equipo.unique())
        respuesta_tipo = TipoEquipo.validar_registro_masivo(nombres_tipo_equipo, prohibir_duplicados_tipos)

        resultado_tipos = respuesta_tipo['resultado']
        if resultado_tipos:
            mensajes_error.extend(respuesta_tipo['errores'])

        respuesta_laboratorios = Laboratorio.validar_registro_masivo(df_equipos[['laboratorio']], prohibir_duplicados_laboratorios)
        resultado_laboratorios = respuesta_laboratorios['resultado']
        if resultado_laboratorios:
            mensajes_error.extend(respuesta_laboratorios['errores'])

        if prohibir_duplicados_equipos and (equipos_nuevos & equipos_actuales):
            mensajes_error.append({'modelo':'Hay equipos ya registrados'})

        if len(mensajes_error) > 0:
            respuesta.update({'resultado':False, 'errores':mensajes_error})

        return respuesta

    @staticmethod
    def registro_masivo(df_equipos: pd.DataFrame,
        prohibir_duplicados_equipos:bool=False,
        prohibir_duplicados_tipos: bool=False,
        prohibir_duplicados_laboratorios: bool=False) -> None:


        respuesta = Equipo.validar_registro_masivo(df_equipos, prohibir_duplicados_equipos, prohibir_duplicados_tipos, prohibir_duplicados_laboratorios)
        resultado = respuesta['resultado']
        errores = respuesta['errores']
        datos = respuesta['datos']

        if resultado:
            df_tipos_simplificado = TipoEquipo.obtener_nombres_cargue_masivo_data_frame(datos)
            TipoEquipo.registro_masivo(df_tipos_simplificado, prohibir_duplicados_tipos)
            Laboratorio.registro_masivo(datos[['laboratorio']], prohibir_duplicados_laboratorios)


            for index, row in datos.iterrows():
               pass



class CompraEquipo(ModeloBase):
    tipo_equipo = models.ForeignKey(
        TipoEquipo,
        related_name="compras_realizadas",
        verbose_name="Tipos de equipos comprados",
        on_delete=models.PROTECT
    )
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad de tipo de equipos comprados", validators=[MinValueValidator(1)])
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
    nombre = models.CharField(
        max_length=60,
        verbose_name="Campo extra con información adicional",
        validators=[RegexValidator(regex=r"((_| |)(\d)+$)", inverse_match=True)],
        unique=True
    )

    def __str__(self) -> str:
        return f'{self.nombre}'


    @staticmethod
    def obtener_por_listado_nombres(lista_nombres: List[str]) -> 'QuerySet[CampoExtra]':
        from django.db.models import Q
        filtro_nombre = Q()
        for nombre in lista_nombres:
            filtro_nombre |= Q(nombre__iexact=nombre)
        return CampoExtra.obtener_todos().filter(filtro_nombre)

    @staticmethod
    def existe_por_nombre(nombre: str) -> bool:
        return CampoExtra.obtener_todos().filter(nombre=nombre).exists()

    @staticmethod
    def registro_masivo(listado_campos: List[str]) -> None:
        import re

        campos_extra_relacionados = [re.sub(r"(_|)(\d)+$", "", campo.upper()) for campo in listado_campos] #Elimino los _<numero> al final de los nombres
        for campo in campos_extra_relacionados:
            if not CampoExtra.existe_por_nombre(campo):
                CampoExtra.objects.create(nombre=campo)


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


@receiver(pre_save, sender=CampoExtra)
def guardar_mayuscula_campos(sender, instance, *args, **kwargs):
    instance.nombre = instance.nombre.upper()

@receiver(pre_save, sender=TipoEquipo)
def guardar_mayuscula_tipos(sender, instance, *args, **kwargs):
    instance.nombre = instance.nombre.upper()